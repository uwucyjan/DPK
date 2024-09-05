import pandas as pd
import time

start = time.time()

nkursow = []

stopread = (pd.read_csv('CSV_Przystanki.csv'))

# funkcje odczytu plików
stops = pd.concat(map(pd.read_csv, ['stops_a.txt','stops_t.txt']),ignore_index=True)
stops.to_csv('stops.csv')
stops = pd.read_csv('stops.csv',usecols=['stop_id','stop_name'])
print('Przetworzono plik Stops.csv')

stop_t = pd.concat(map(pd.read_csv, ['stop_times_a.txt','stop_times_t.txt']),ignore_index=True)
stop_t.to_csv('stop_t.csv')
stop_t = pd.read_csv('stop_t.csv',usecols=['stop_id','trip_id','stop_sequence'])
print('Przetworzono plik Stop_t.csv')

for idx, row in stopread.iterrows():

    stopname = str(row['Name'])
    stopname = stopname.replace('"', "'")

    # wybór grupy przystanków po nazwie
    stopids = stops.loc[(stops['stop_name'] == stopname)]

    if stopids.empty:
        stopname = (str(stopname)+' (nż)')
        stopids = stops.loc[(stops['stop_name'] == stopname)]
        if stopids.empty:
            print('BŁĄD: BRAK KURSÓW NA PRZYSTANKU',stopname)

    for n in range(len(stopids)):

        # wybierz kolejne id przystanku
        stopid = stopids['stop_id'].iloc[n]

        # wyfiltruj zatrzymania na grupie przystanków
        st = stop_t[(stop_t['stop_id'] == stopid)]

        for m in range(0, len(st)):

            # id kursu
            tripid = st.iloc[m]

            # wybór kursów w dzień tygodnia / sobotę / święto
            if "service_1" in tripid['trip_id']:

                # ile kurs ma przytsanków
                nstops = (tripid['stop_sequence']) - 1

                nkursow.append(nstops)

    DP = int(len(nkursow))

    # wartość przystanku

    DPK = round((sum(nkursow)) / 1000, 3)

    print(stopread.loc[idx])
    input()

    stopread.loc[idx, ['DPK']] = [DPK]

    #print((stopread.loc[idx])['Name'],'-',(stopread.loc[idx])['DPK'])
    print(round(int(idx)/int(len(stopread))*100,1),'%')

    nkursow.clear()

stopread.to_csv('CSV_Przystanki.csv')

end = time.time()

print((end - start)/60)