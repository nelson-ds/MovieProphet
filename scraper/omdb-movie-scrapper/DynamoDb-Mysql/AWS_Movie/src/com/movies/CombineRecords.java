package com.movies;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class CombineRecords {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		String csvFile = "comb_wiki_bom_omdb_final.csv";
		BufferedWriter	bw = null;
		FileWriter fw = null;
		//	bom_title	key_bom	key_omdb	key_wiki	omdb_title	score	wiki_title	year_bom	
		//year_bom_format	year_omdb	year_omdb_format	year_wiki	year_wiki_format
		fw = new FileWriter("movie.tsv");
		bw = new BufferedWriter(fw);
		
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        int index = 0;

        try {

            br = new BufferedReader(new FileReader(csvFile));
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] country = line.split(cvsSplitBy);
                
                String year = "";
                
                try{
                	int data = Integer.parseInt(country[10]);
                	year = data + "";
                }catch(NumberFormatException ex){
                	year = country[10];
                }
                
                bw.write(country[3] + "\t" + country[5] + "\t" + year);
                bw.newLine();

            }
            bw.flush();
            bw.close();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
	}
}