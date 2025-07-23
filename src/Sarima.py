import mosqlient
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
from datetime import datetime
from epiweeks import Week
import gc


states = ['MG']

def load_data(df, state, start_date="2017-02-01", end_date="2025-04-01"):
    # Filtrar e processar de forma eficiente
    df_filtered = df[df['uf'] == state]
    if df_filtered.empty:
        return df_filtered.copy()
    # Converter tipos apenas se necessário
    if not pd.api.types.is_datetime64_any_dtype(df_filtered['date']):
        df_filtered = df_filtered.copy()
        df_filtered['date'] = pd.to_datetime(df_filtered['date'], format='%Y-%m-%d', errors='coerce')
    if not pd.api.types.is_numeric_dtype(df_filtered['casos']):
        df_filtered = df_filtered.copy()
        df_filtered['casos'] = pd.to_numeric(df_filtered['casos'], errors='coerce')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_filtered = df_filtered[(df_filtered['date'] >= start_date) & (df_filtered['date'] <= end_date)]
    df_filtered = df_filtered.dropna(subset=['date', 'casos'])
    df_filtered = df_filtered.sort_values(by='date')
    return df_filtered.reset_index(drop=True)

def get_epiweek_dates(start_year, start_week, end_year, end_week):
    """
    Generate dates for epidemiological weeks from start_week/start_year to end_week/end_year
    Using the epiweeks library for accurate conversion
    """
    dates = []
    
    current_year = start_year
    current_week = start_week
    
    while True:
        # Use epiweeks library for accurate date conversion
        try:
            week_obj = Week(current_year, current_week)
            dates.append(week_obj.startdate())
        except:
            # Fallback if week doesn't exist (e.g., week 53 in some years)
            if current_week > 52:
                current_week = 1
                current_year += 1
                continue
        
        # Check if we've reached the end
        if current_year == end_year and current_week == end_week:
            break
            
        # Move to next week
        current_week += 1
        if current_week > 52:
            current_week = 1
            current_year += 1
            
    return dates

def preprocess_data(df):
    # Processar agrupamento de forma eficiente
    if df.empty:
        return pd.DataFrame(columns=['date', 'cases'])
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    df = df.dropna(subset=['date', 'casos'])
    df_grouped = df.groupby('date', as_index=False)['casos'].sum()
    df_grouped = df_grouped.rename(columns={'casos': 'cases'})
    return df_grouped.sort_values(by='date').reset_index(drop=True)

api_key = "rick0110:414cf362-4ca0-4a50-84ff-e432ff083471"

arquivo = "./../data/dengue.csv.gz"
colunas = ["date", "casos", "uf"]



validations = {'validation1': [(2010, 40), (2022, 25), (2022, 41), (2023, 40)],
              'validation2': [(2010, 40), (2023, 25), (2023, 41), (2024, 40)],
              'validation3': [(2010, 40), (2024, 25), (2024, 41), (2025, 40)],
              'forecast': [(2010, 40), (2025, 25), (2025, 41), (2026, 40)]}

for validation, weeks in validations.items():
    train_start, train_end = weeks[0], weeks[1]
    validation_start, validation_end = weeks[2], weeks[3]
    print(f'Initializing {validation} with training from EW {train_start[1]} {train_start[0]} to EW {train_end[1]} {train_end[0]} and validation from EW {validation_start[1]} {validation_start[0]} to EW {validation_end[1]} {validation_end[0]}')
    
    for state in states:
        print(f"Processing state: {state}")
        start_date = str(Week(train_start[0], train_start[1]).startdate())
        end_date = str(Week(train_end[0], train_end[1]).enddate())
        print("".join(['=']*20))
        print('Loading data...')
        df_temp = pd.read_csv(
            arquivo,
            usecols=colunas,
            compression='gzip',
            dtype={'uf': str, 'casos': 'float32'},
            parse_dates=['date'],
            low_memory=True
        )
    
        df_state = df_temp[(df_temp['uf'] == state) & 
                          (df_temp['date'] >= start_date) & 
                          (df_temp['date'] <= end_date)].copy()
        print(f"Data loaded successfully")
        
        del df_temp
        
        if df_state.empty:
            print(f"No data for {state} in period. Skipping.")
            del df_state, start_date, end_date
            continue
        df_sel_weekly = preprocess_data(df_state)
        del df_state, start_date, end_date
        gc.collect()
        
        if len(df_sel_weekly) < 52:
            print(f"Not enough data for {state}. Skipping.")
            del df_sel_weekly
            continue
            
        train = np.log(df_sel_weekly['cases']+0.1).values
        del df_sel_weekly
        
        model1 = SARIMAX(train, order=(2, 1, 2), seasonal_order=(2, 1, 2, 52), 
                       enforce_invertibility=False, enforce_stationarity=False)
        model1_fit = model1.fit(disp=False, maxiter=100)
        del train, model1
        
        epiweek_dates = get_epiweek_dates(validation_start[0], validation_start[1], 
                                        validation_end[0], validation_end[1])
        
        forecast = model1_fit.get_forecast(steps=52)
        
        conf_int_95 = forecast.conf_int(alpha=0.05)
        conf_int_90 = forecast.conf_int(alpha=0.10)
        conf_int_80 = forecast.conf_int(alpha=0.20)
        conf_int_50 = forecast.conf_int(alpha=0.50)
        
        pred = np.exp(forecast.predicted_mean) - 0.1
        del forecast
        gc.collect()

        lower_95 = np.exp(conf_int_95[:, 0]) - 0.1
        upper_95 = np.exp(conf_int_95[:, 1]) - 0.1
        del conf_int_95
        gc.collect()
        
        lower_90 = np.exp(conf_int_90[:, 0]) - 0.1
        upper_90 = np.exp(conf_int_90[:, 1]) - 0.1
        del conf_int_90
        gc.collect()
        
        lower_80 = np.exp(conf_int_80[:, 0]) - 0.1
        upper_80 = np.exp(conf_int_80[:, 1]) - 0.1
        del conf_int_80
        
        lower_50 = np.exp(conf_int_50[:, 0]) - 0.1
        upper_50 = np.exp(conf_int_50[:, 1]) - 0.1

        epiweeks = []
        years = []
        current_year = validation_start[0]
        current_week = validation_start[1]
        
        for _ in range(52):
            epiweeks.append(current_week)
            years.append(current_year)
            current_week += 1
            if current_week > 52:
                current_week = 1
                current_year += 1

        forecast_df = pd.DataFrame({
            'date': epiweek_dates,
            'lower_95': lower_95,
            'lower_90': lower_90,
            'lower_80': lower_80,
            'lower_50': lower_50,
            'pred': pred,
            'upper_50': upper_50,
            'upper_80': upper_80,
            'upper_90': upper_90,
            'upper_95': upper_95
        })
        
        del lower_95, upper_95, lower_90, upper_90, lower_80, upper_80, lower_50, upper_50, pred
        gc.collect()
        
        forecast_df['epiweek'] = epiweeks
        forecast_df['year'] = years
        del epiweeks, years
        gc.collect()
        
        numeric_cols = ['lower_95', 'lower_90', 'lower_80', 'lower_50', 'pred', 
                      'upper_50', 'upper_80', 'upper_90', 'upper_95']
        forecast_df[numeric_cols] = forecast_df[numeric_cols].clip(lower=0)
        del numeric_cols
        gc.collect()
        
        forecast_df = forecast_df[['date', 'year', 'epiweek', 'lower_95', 'lower_90', 
                                 'lower_80', 'lower_50', 'pred', 'upper_50', 'upper_80', 
                                 'upper_90', 'upper_95']]
        
        os.makedirs('./forecasts', exist_ok=True)
        output_file = f'./forecasts/{state}_dengue_forecast_{validation}_EW{validation_start[1]}_{validation_start[0]}_to_EW{validation_end[1]}_{validation_end[0]}.csv'
        forecast_df.to_csv(output_file, index=False)

        res = mosqlient.upload_prediction(
        model_id = 107, 
        description = 'test for sprint 2025 preds of Sarima', 
        commit = None,
        predict_date = '2025-07-22', 
        prediction = forecast_df,
        adm_1=state,
        api_key = api_key)


        
        print(f"✅ Forecast saved for {state}: {output_file}")

        del forecast_df, model1_fit, epiweek_dates, output_file
        import gc
        gc.collect()
        
    