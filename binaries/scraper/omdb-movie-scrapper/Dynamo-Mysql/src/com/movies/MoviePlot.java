package com.movies;

import java.io.IOException;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;

public class MoviePlot {

	public static void main(String[] args) throws IOException, SQLException {

		ScanResult result = null;
		String tableName = "movieratings-omdb";

		String plotQuery = " insert into omdb_movies (movie_id, plot) values (?, ?)";
		PreparedStatement plotstmt = DBConnection.getConnection().prepareStatement(plotQuery);
		int movie_index = 0;
		
		String movieQuery = " SELECT movie_id FROM omdb_movies WHERE year=? AND title=?";
		PreparedStatement moviestmt = DBConnection.getConnection().prepareStatement(movieQuery);
		
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
				moviestmt.setInt(1, Integer.parseInt(map.get("year").getN()));
				moviestmt.setString(2, map.get("title").getS());
				
				ResultSet rs = moviestmt.executeQuery();
				int movie_id = 0;
				
				if(rs != null){
					while(rs.next()){
						movie_id = rs.getInt("movie_id");
					}
				}
				
				rs.close();
				
				String column = "plot";
				if(map.containsKey(column) && map.get(column) != null && map.get(column).getS() != null){
					plotstmt.setInt(1, movie_id);
					plotstmt.setString(2, map.get(column).getS());
					plotstmt.addBatch();
				}
			}

			plotstmt.executeBatch();
			System.out.println(movie_index);

			if(plotstmt != null){
				plotstmt.close();
			}

		} while(result.getLastEvaluatedKey() != null);
		
		if(moviestmt != null){
			moviestmt.close();
		}
		
		if(plotstmt != null){
			plotstmt.close();
		}

		try{
			DBConnection.getConnection().close();
		}catch(SQLException ex){
			ex.printStackTrace();
		}


		return;
	}
}