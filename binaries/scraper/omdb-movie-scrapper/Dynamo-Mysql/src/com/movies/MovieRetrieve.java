package com.movies;

import java.io.IOException;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;

public class MovieRetrieve {

	public void fillData(String column, Map<String, AttributeValue> map, PreparedStatement pstmt, int colIndex)
			throws SQLException{
		if(map.containsKey(column) && map.get(column) != null && map.get(column).getS() != null){
			pstmt.setString(colIndex, map.get(column).getS());
		}else{
			pstmt.setString(colIndex, null);
		}
	}

	public static void main(String[] args) throws IOException, SQLException {
		MovieRetrieve mr = new MovieRetrieve();

		ScanResult result = null;
		String tableName = "movieratings-omdb";

		String movieQuery = " insert into omdb_movies (movie_id, movie_year, title, rated, response, language, "
				+ "country, metascore, imdbrating, released, runtime, type, poster, imdbvotes, awards) "
				+ "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
		int movie_index = 1;



		do{

			//			Path file_last_movie = Paths.get("last.txt");

			//			if(file_last_movie.toFile().exists()){
			//				reader = new BufferedReader(new FileReader(file_last_movie.toFile()));
			//				String line = reader.readLine();
			//				while ( line != null ) {
			//					line = reader.readLine();
			//					movie_index = new Integer(line);
			//					break;
			//				}
			//			}

			ScanRequest req = new ScanRequest().withTableName(tableName);

			if(result != null){
				req.setExclusiveStartKey(result.getLastEvaluatedKey());
			}
			Connection.client.scan(req);
			result = Connection.client.scan(req);
			System.out.println("Number of records ==============>" + result.getItems().size());

			List<Map<String, AttributeValue>> rows = result.getItems();
			PreparedStatement movieStmt = DBConnection.getConnection().prepareStatement(movieQuery);

			for(Map<String, AttributeValue> map : rows){
				movieStmt.setInt(1, movie_index);
				movieStmt.setInt(2, Integer.parseInt(map.get("year").getN()));

				String[] columns = {"title","rated","response","language","country","metascore",
						"imdbrating", "released","runtime","type","poster","imdbvotes","awards"};
				int colIndex = 3;
				for(String column:columns){
					mr.fillData(column, map, movieStmt, colIndex);
					colIndex++;
				}

				movieStmt.addBatch();

				movie_index++;
			}

			movieStmt.executeBatch();
			System.out.println(movie_index);

			if(movieStmt != null){
				movieStmt.close();
			}

		} while(result.getLastEvaluatedKey() != null);


		try{
			DBConnection.getConnection().close();
		}catch(SQLException ex){
			ex.printStackTrace();
		}


		return;
	}
}