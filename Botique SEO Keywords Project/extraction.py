import pandas as pd


def getSeoResults(filename,paramDict):
    try:
        df = pd.read_csv("./DataFiles/"+filename,encoding="UTF-16",sep='\t')
        
        # Check respected columns to be existed
        try:
            
             df = df[['Keyword','Difficulty','Volume','Country']]
        
        except:
            
            return "Invalid Columns"
        
        try:
            df.dropna(axis=0,inplace=True)


            # Most Searched #
            df_ms = df[(df['Volume']>=paramDict['most_searched_min_volume']) & (df['Volume']<=paramDict['most_searched_max_volume']) & (df['Difficulty']>=paramDict['most_searched_min_diff']) & (df['Difficulty']<=paramDict['most_searched_max_diff'])]
            df_ms_Keywords = df_ms['Keyword'].tolist()
            df_ms_Difficulty = df_ms['Difficulty'].tolist()
            df_ms_Volume = df_ms['Volume'].tolist()
            df_ms_Country = df_ms['Country'].tolist()

            #################


            # ROI #
            df_roi = df[(df['Volume']>=paramDict['roi_min_volume']) & (df['Volume']<=paramDict['roi_max_volume']) & (df['Difficulty']>=paramDict['roi_min_diff']) & (df['Difficulty']<=paramDict['roi_max_diff'])]
            df_roi_Keywords = df_roi['Keyword'].tolist()
            df_roi_Difficulty = df_roi['Difficulty'].tolist()
            df_roi_Volume = df_roi['Volume'].tolist()
            df_roi_Country = df_roi['Country'].tolist()

          
            #######


            # Easy Wins #
            df_ew = df[(df['Volume']>=paramDict['easy_wins_min_volume']) & (df['Volume']<=paramDict['easy_wins_max_volume']) & (df['Difficulty']>=paramDict['easy_wins_min_diff']) & (df['Difficulty']<=paramDict['easy_wins_max_diff'])]
            df_ew_Keywords = df_ew['Keyword'].tolist()
            df_ew_Difficulty = df_ew['Difficulty'].tolist()
            df_ew_Volume = df_ew['Volume'].tolist()
            df_ew_Country = df_ew['Country'].tolist()

       
            #############


            # Biggest Traffic Oppurtunities
            df_bto = df[(df['Volume']>=paramDict['big_traffic_min_volume']) & (df['Volume']<=paramDict['big_traffic_max_volume']) & (df['Difficulty']>=paramDict['big_traffic_min_diff']) & (df['Difficulty']<=paramDict['big_traffic_max_diff'])]
            df_bto_Keywords = df_bto['Keyword'].tolist()
            df_bto_Difficulty = df_bto['Difficulty'].tolist()
            df_bto_Volume = df_bto['Volume'].tolist()
            df_bto_Country = df_bto['Country'].tolist()
            

            ###############################
            
            writer = pd.ExcelWriter('./OutputFiles/outputFile.xlsx', engine='xlsxwriter')
            # Write each dataframe to a different worksheet.
            df_ms.to_excel(writer, sheet_name='Most Searched')
            df_roi.to_excel(writer, sheet_name='Highest ROI')
            df_ew.to_excel(writer, sheet_name='Easy Wins')
            df_bto.to_excel(writer, sheet_name='Biggest Traffic Oppurtunities')

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()

            ###############################
            return [df_ms_Keywords,df_ms_Difficulty,df_ms_Volume,df_roi_Keywords,df_roi_Difficulty,df_roi_Volume,df_ew_Keywords,df_ew_Difficulty,df_ew_Volume,df_bto_Keywords, df_bto_Difficulty,df_bto_Volume,df_ms_Country,df_roi_Country,df_ew_Country,df_bto_Country]

        except Exception as e:
            print(e)
            return "Invalid Error occured"

    except:
        return "Invalid File"
