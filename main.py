from json import dumps, load
from folium import Choropleth, Map
from numpy import log, linspace
from pandas import DataFrame, read_excel
from os import system


class Excel_to_Map():

    def __init__(self):
        self.geo_str = dumps(load(open("harita.json", "r", encoding="utf-8")))  # JSON şeklindeki haritamızı açtık.
        self.excel = DataFrame(read_excel("Kitap1.xlsx"))  # Excel dosyamızı açtık.

    def makeamap(self, tablo, saveas):
        '''
        Bu fonksiyon verilen bir excel'deki istenilen bir tabloyu haritalandırır ve istenilen isimde bir html dosyası haline getirip açar.
        '''
        maptr = Map(location=[39, 35], zoom_start=7, TileLayer="Mapbox Bright",)  # Türkiye üzerine zoom yaparak başlayalım.
        
        # Excel tablomuzu harita yapan arkadaşın alayabileceği hale çevirelim.
        excel = self.excel  # Excel Belgemizi bozmamak için kopyasını aldık.
        excel[tablo] = log(excel[tablo].tolist())
        scale = linspace(excel[tablo].min(), excel[tablo].max(), 6, dtype=object).tolist()

        # Harita yapmaya başlayalım:
        Choropleth(
            geo_data=self.geo_str,
            data=excel,
            name=tablo,
            threshold_scale=scale,
            columns=["İl", tablo],
            key_on="feature.properties.name",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name=tablo,
        ).add_to(maptr)

        maptr.save(f"{saveas}.html")  # Haritayı kaydedelim.
        system(f"start {saveas}.html")  # Haritayı açalım.

if __name__ == "__main__":
    homework = Excel_to_Map()
    homework.makeamap("Nüfus", "nufus")
    homework.makeamap("Kişi başına yıllık gelir (USD)", "kbyg")