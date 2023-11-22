import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Wczytaj dane z pliku Excela
df = pd.read_excel('sym.xlsx')

# Pytaj użytkownika o wybór pisma
wybrane_pismo = st.selectbox("Wybierz pismo:", df['pismo'].unique(), index=df['pismo'].tolist().index('Twój Styl'))

# Filtruj ramkę danych dla wybranego pisma
df_pismo = df[df['pismo'] == wybrane_pismo]

st.write(f'RPC pisma: {df_pismo.iloc[0, 6].round(1)}    RPC grupy: {df_pismo.iloc[0, 7].round(1)}')
st.write(f'CPW do mediaplanu (VII 2022 - VI 2023): {df_pismo.iloc[0, 10].round(2)}')
st.write(f'CPW po zmianie segmentacji (VII 2022 - VI 2023): {df_pismo.iloc[0, 9].round(2)}')


kolumny_emisji = ['1 emisja', '2 emisje', '3 emisje', '4 emisje', '5 emisje', '6 emisje', '7 emisji',
                  '8 emisji', '9 emisji', '10 emisji']

kolumny_emisji_2 = [col + '.1' for col in kolumny_emisji]

kolumny_emisji_3 = [col + '.2' for col in kolumny_emisji]

# Wybierz dane dotyczące emisji
emisje = df_pismo[kolumny_emisji]
emisje = emisje.transpose()

emisje_2 = df_pismo[kolumny_emisji_2]
emisje_2 = emisje_2.transpose()

emisje_3 = df_pismo[kolumny_emisji_3]
emisje_3 = emisje_3.transpose()

kolory = ['#00AADB', '#981923', '#193441', '#E0404B']


#plt.figure(figsize=(25, 20))

# Dopasuj wielomian do danych
degree = 2  # Stopień wielomianu
coefficients = np.polyfit(range(1, 11), emisje.iloc[:, 0], degree)
smoothed_values = np.linspace(1, 10, 10)
smoothed_emisje = np.polyval(coefficients, smoothed_values)

coefficients_3 = np.polyfit(range(1, 11), emisje_3.iloc[:, 0], degree)
smoothed_emisje_3 = np.polyval(coefficients_3, smoothed_values)

# Zabezpiecz przed malejącą funkcją
for i in range(9):
    if smoothed_emisje[i + 1] < smoothed_emisje[i]:
        smoothed_emisje[i + 1] = smoothed_emisje[i]
    if smoothed_emisje_3[i + 1] < smoothed_emisje_3[i]:
        smoothed_emisje_3[i + 1] = smoothed_emisje_3[i]

if smoothed_emisje[0] > df_pismo.iloc[0, 9]:
    smoothed_emisje = smoothed_emisje - (smoothed_emisje[0] - df_pismo.iloc[0, 9])

if smoothed_emisje_3[0] > df_pismo.iloc[0, 10]:
    smoothed_emisje_3 = smoothed_emisje_3 - (smoothed_emisje_3[0] - df_pismo.iloc[0, 10])

plt.plot(smoothed_values, smoothed_emisje, 'o-', label='Symulacja (nowa segmentacja)', color=kolory[0])
plt.plot(smoothed_values, smoothed_emisje_3, 'o-', label='Symulacja (aktualna segmentacja)', color=kolory[2])
#plt.plot(range(1, 11), emisje_2.iloc[:, 0], 'o-', label='Rozkłady Bernouillego', color=kolory[1])

plt.ylabel('OTS(1+)')
plt.xlabel('L.emisji')
plt.xticks(range(1, 11), [f'{i}' for i in range(1, 11)])  # Dodaj etykiety na osi X
plt.legend(title='Typ danych', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.legend(title='Typ danych')
st.pyplot(plt)


# Wybierz kolumny z danymi dotyczącymi wydań
wydania = df_pismo[['1 wydanie', '2 wydania', '3 wydania', '4 wydania']]

# Przekształć procenty na liczby zmiennoprzecinkowe
wydania = wydania.apply(lambda x: x.astype('float') / 100.0)

# Sumuj wartości dla każdego wydania
suma_wydania = wydania.sum()


# Twórz wykres kołowy z dodanymi kolorami
fig, ax = plt.subplots()
ax.pie(suma_wydania, labels=suma_wydania.index, autopct='%1.1f%%', startangle=90, colors=kolory)
st.pyplot(fig)
