import numpy as np
import pandas as pd
import ScraperFC as sfc
from selenium import webdriver

scraper = sfc.FBRef()
scraper.driver = webdriver.Chrome()


all_stat_categ = ['standard', 'goalkeeping', 'advanced goalkeeping', 'shooting', 
            'passing', 'pass types', 'goal and shot creation', 'defensive', 'possession', 'playing time', 'misc']


def reasignar_nombres_columnas(df):
    # obtener nombres columnas
    nombres_col = []
    for tup in df.columns[:-2]:
        n1, n2 = tup
        nombres_col.append(n2)

    for tup in df.columns[-2:]: # player link y player ID
        n1, n2 = tup
        nombres_col.append(n1)

    print( nombres_col )
    print(len(nombres_col))

    # reasignar nombres en el dataframe
    df.columns = nombres_col

    return df


def scrapear_por_categoria(anio:int, liga:str, categorias:list):

    for categ in categorias:
        
        # tupla (estad_equipo, estad_oponent, estad_jugadores)
        tupla = scraper.scrape_stats(year=anio, league=liga, stat_category=categ, normalize=False)

        # EQUIPOS -------------------
        # sacar df
        df_eq = tupla[0].copy()  # es el 1º de la tupla
        # renombrar columnas
        df_eq = reasignar_nombres_columnas(df_eq)
        # poner indice ID
        df_eq.set_index('Team ID', inplace=True)
        # pasar a csv
        df_eq.to_csv(f'data/UCL_{anio}/est_equipos/{categ}.csv', index=True)

        
        # JUGADORES -----------------
        # sacar df
        df_jug = tupla[2].copy()  # es el 3º de la tupla
        # renombrar columnas
        df_jug = reasignar_nombres_columnas(df_jug) 
        # indice ID
        df_jug.set_index('Player ID', inplace=True)
        # pasar a csv
        df_jug.to_csv(f'data/UCL_{anio}/est_jugadores/{categ}.csv', index=True)



if __name__ == '__main__':

    categorias_interes = ['standard', 'goalkeeping', 'shooting', 'goal and shot creation']

    scrapear_por_categoria(anio=2023, liga='Champions League', categorias=categorias_interes)
    
    scrapear_por_categoria(anio=2024, liga='Champions League', categorias=categorias_interes)
