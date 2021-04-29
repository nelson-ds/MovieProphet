package com.movies;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;

public class ADD_KEY_Movie {

	public static void main(String[] args) throws SQLException {
		ScanResult result = null;
		String tableName = "movieratings-omdb";
		
		String movieQuery = " SELECT movie_id FROM omdb_movies WHERE year=? AND title=?";
		PreparedStatement moviestmt = DBConnection.getConnection().prepareStatement(movieQuery);
		
		String actorQuery = " SELECT actor_id FROM omdb_actors WHERE actor_name=?";
		PreparedStatement actstmt = DBConnection.getConnection().prepareStatement(actorQuery);
		
		String movieActorQuery = "INSERT INTO omdb_movie_actor(movie_id,actor_id) VALUES (?,?)";
		PreparedStatement mapstmt = DBConnection.getConnection().prepareStatement(movieActorQuery);

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
				
				if(map.containsKey("actors") && map.get("actors") != null && map.get("actors").getL() != null){
					for(AttributeValue attr:map.get("actors").getL()){
						if(attr.getS() != null){
							actstmt.setString(1, attr.getS());
							int actor_id = 0;
							ResultSet actrs = actstmt.executeQuery();
							if(actrs != null){
								while(actrs.next()){
									actor_id = actrs.getInt("actor_id");
								}
							}
							
							actrs.close();
							
							mapstmt.setInt(1, movie_id);
							mapstmt.setInt(2, actor_id);
							mapstmt.addBatch();
						}
					}
				}
			}
			
			mapstmt.executeBatch();

		} while(result.getLastEvaluatedKey() != null);
		
		if(moviestmt != null){
			moviestmt.close();
		}
		
		if(actstmt != null){
			actstmt.close();
		}
		
		if(mapstmt != null){
			mapstmt.close();
		}

		try{
			DBConnection.getConnection().close();
		}catch(SQLException ex){
			ex.printStackTrace();
		}


		return;
	}
}