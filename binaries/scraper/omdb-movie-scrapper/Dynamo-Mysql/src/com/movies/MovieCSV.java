package com.movies;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;

public class MovieCSV {

	public void fillData(String column, Map<String, AttributeValue> map, BufferedWriter bw) throws IOException{
		System.out.println(map);
		if(map.containsKey(column)){
			if(map.get(column) != null && map.get(column).getS() != null){
				bw.write(map.get(column).getS());
			}else{
				bw.write("");
			}
		}
		bw.write("\t");
	}

	public void fillListData(String column, Map<String, AttributeValue> map, BufferedWriter bw) throws IOException{
		if(map.containsKey(column) && map.get(column) != null){
			for(int i = 0; i < map.get(column).getL().size(); i++){
				if(map.get(column).getL().get(i) != null && map.get(column).getL().get(i).getS() != null){
					bw.write(map.get(column).getL().get(i).getS());
				}
				if(i != map.get(column).getL().size()-1){
					bw.write(",");
				}
			}
		}else{
			bw.write("");
			bw.write("\t");
		}
	}

	public static void main(String[] args) throws IOException, SQLException {
		MovieCSV csv = new MovieCSV();

		ScanResult result = null;
		String tableName = "movieratings-omdb";

		//		BufferedReader reader = null;
		BufferedWriter	bw = null;
		FileWriter fw = null;

		fw = new FileWriter("omdb.tsv");
		bw = new BufferedWriter(fw);

		bw.write("index\tyear\ttitle\tplot\trated\response\tlanguage\tcountry\tmetascore\timdbrating\treleased\t"
				+ "runtime\ttype\tposter\timdbvotes\timdbid\tawards\tactors\tdirectors\twriters\tgenres");
		bw.newLine();

		int movie_index = 1;

		do{

			ScanRequest req = new ScanRequest().withTableName(tableName);

			if(result != null){
				req.setExclusiveStartKey(result.getLastEvaluatedKey());
			}
			Connection.client.scan(req);
			result = Connection.client.scan(req);
			System.out.println("Number of records ==============>" + result.getItems().size());

			List<Map<String, AttributeValue>> rows = result.getItems();



			for(Map<String, AttributeValue> map : rows){
				bw.write(((Integer)movie_index).toString());
				bw.write("\t");
				bw.write(Integer.parseInt(map.get("year").getN()));
				bw.write("\t");

				String[] columns = {"title","plot","rated","response","language","country","metascore",
						"imdbrating", "released","runtime","type","poster","imdbvotes","imdbid","awards"};
				for(String column:columns){
					csv.fillData(column, map, bw);
				}

				String[] listColumns = {"actors","directors","writers"};
				for(String column:listColumns){
					csv.fillListData(column, map, bw);
				}

				if(map.containsKey("genres") && map.get("genres") != null){
					for(int i = 0; i < map.get("genres").getL().size(); i++){
						if(map.get("genres").getL().get(i) != null){
							bw.write(map.get("genres").getL().get(i).getS());
						}

						if(i != map.get("genres").getL().size()-1){
							bw.write(",");
						}
					}
				}
				bw.newLine();

				movie_index++;
			}

			bw.flush();
			System.out.println(movie_index);

		} while(result.getLastEvaluatedKey() != null);

		bw.close();
		return;
	}
}