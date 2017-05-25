package com.movies;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Convertor {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		Path path = Paths.get("/Users/saurabhseth/Development/capstone/common.csv");
		BufferedReader br = new BufferedReader(new FileReader(path.toFile()));
		
		BufferedWriter	bw = null;
		FileWriter fw = null;

		fw = new FileWriter("common-final.tsv");
		bw = new BufferedWriter(fw);

//		bw.write("movie_year\ttitle\treleased\tkey_omdb");
//		bw.newLine();
		
		String line = null;
		while((line = br.readLine()) != null){
			String[] columns = line.split(",");
			bw.write(columns[0]+"\t"+columns[1]+"\t"+columns[2]);
			bw.newLine();
		}
		
		bw.flush();
		bw.close();
		
		br.close();
		
	}

}
