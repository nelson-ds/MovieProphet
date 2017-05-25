package com.movies;

import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Table;

public class MovieDeleteTable {

	public static void main(String[] args) throws Exception {

		Table table = new DynamoDB(Connection.client).getTable("MovieRatings");
		try {
			System.out.println("Attempting a table delete...");
			table.delete();
			table.waitForDelete();
			System.out.print("Success.");

		} catch (Exception e) {
			System.err.println("Unable to delete Item: ");
			System.err.println(e.getMessage());
		}
	}
}