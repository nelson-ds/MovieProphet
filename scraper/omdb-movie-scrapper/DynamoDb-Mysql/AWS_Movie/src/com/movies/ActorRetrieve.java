package com.movies;

import java.io.IOException;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.amazonaws.services.dynamodbv2.model.AttributeValue;
import com.amazonaws.services.dynamodbv2.model.ScanRequest;
import com.amazonaws.services.dynamodbv2.model.ScanResult;

public class ActorRetrieve {

	public static void main(String[] args) throws IOException, SQLException {

		ScanResult result = null;
		String tableName = "movieratings-omdb";

		Set<String> actors = new HashSet<>();

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
				
				if(map.containsKey("actors") && map.get("actors") != null && map.get("actors").getL() != null){
					for(AttributeValue attr:map.get("actors").getL()){
						if(attr.getS() != null){
							actors.add(attr.getS());
						}
					}
				}
			}

		} while(result.getLastEvaluatedKey() != null);
		
		System.out.println(actors.size());
		
		
		String actorQuery = " insert into omdb_actors (actor_id, actor_name) values (?, ?)";
		PreparedStatement actorStmt = DBConnection.getConnection().prepareStatement(actorQuery);
		
		int actor_index = 1;
		
		for(String actor:actors){
			actorStmt.setInt(1, actor_index++);
			actorStmt.setString(2, actor);
			actorStmt.addBatch();
		}
		
		actorStmt.executeBatch();
		System.out.println(actor_index);
		
		if(actorStmt != null){
			actorStmt.close();
		}

		try{
			DBConnection.getConnection().close();
		}catch(SQLException ex){
			ex.printStackTrace();
		}


		return;
	}
}