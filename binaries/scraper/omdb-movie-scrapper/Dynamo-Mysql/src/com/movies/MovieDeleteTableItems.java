package com.movies;

import java.util.Iterator;

import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.PrimaryKey;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.document.spec.DeleteItemSpec;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.ListObjectsV2Request;
import com.amazonaws.services.s3.model.ListObjectsV2Result;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.S3ObjectSummary;
import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class MovieDeleteTableItems {

	public static void main(String[] args) throws Exception {

		Table table = new DynamoDB(Connection.client).getTable("movieratings-omdb");
		String bucketName = "bcg-omdb-cleanup";
		AmazonS3 s3Client = new AmazonS3Client(new ProfileCredentialsProvider());

		final ListObjectsV2Request req = new ListObjectsV2Request().withBucketName(bucketName);
		ListObjectsV2Result result;
		do {               
			result = s3Client.listObjectsV2(req);


			for (S3ObjectSummary objectSummary :
				result.getObjectSummaries()) {
				S3Object s3object = s3Client.getObject(new GetObjectRequest(
						bucketName, objectSummary.getKey()));
				System.out.println(s3object.getKey());
				if(s3object.getKey().equals("2005-1.json")){
					int year = 2005;
					JsonParser parser = new JsonFactory()
							.createParser(s3object.getObjectContent());

					JsonNode rootNode = new ObjectMapper().readTree(parser);
					Iterator<JsonNode> iter = rootNode.path("ratings").elements();
					ObjectNode currentNode;
					int count = 0;

					while(iter.hasNext()){
						currentNode = (ObjectNode) iter.next();
						String title = currentNode.path("Title").asText();

						DeleteItemSpec deleteItemSpec = new DeleteItemSpec()
								.withPrimaryKey(new PrimaryKey("year", year, "title", title));


						try {
							System.out.println("Attempting a conditional delete...");
							table.deleteItem(deleteItemSpec);
							System.out.println("DeleteItem succeeded");
							//          	            table.delete();
							//          	            table.waitForDelete();
							//          	            System.out.print("Success.");

						} catch (Exception e) {
							System.err.println("Unable to delete Item: ");
							System.err.println(e.getMessage());
						}
					}
					parser.close();

					break;
				}
			}
		} while(result.isTruncated() == true ); 
	}
}