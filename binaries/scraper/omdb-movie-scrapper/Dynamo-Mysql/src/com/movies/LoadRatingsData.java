package com.movies;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import com.amazonaws.AmazonClientException;
import com.amazonaws.AmazonServiceException;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3Client;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.ListObjectsRequest;
import com.amazonaws.services.s3.model.ListObjectsV2Request;
import com.amazonaws.services.s3.model.ListObjectsV2Result;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.services.s3.model.S3ObjectSummary;

import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

public class LoadRatingsData {

	public static void main(String[] args) throws JsonParseException, IOException {
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
        	   
        	   JsonParser parser = new JsonFactory()
        	            .createParser(s3object.getObjectContent());
        	   
        	   JsonNode rootNode = new ObjectMapper().readTree(parser);
               Iterator<JsonNode> iter = rootNode.path("ratings").elements();
               ObjectNode currentNode;
               int count = 0;
               
               while(iter.hasNext()){

            	   currentNode = (ObjectNode) iter.next();

            	   int year = currentNode.path("Year").asInt();
            	   String title = currentNode.path("Title").asText();
            	   String plot = currentNode.path("Plot").asText();
            	   String rated = currentNode.path("Rated").asText();
            	   Boolean response = currentNode.path("Response").asBoolean();
            	   String language = currentNode.path("Language").asText();
            	   String country = currentNode.path("Country").asText();
            	   String metascore = currentNode.path("Metascore").asText();
            	   String imdbRating = currentNode.path("imdbRating").asText();
            	   String released = currentNode.path("Released").asText();
            	   String runtime = currentNode.path("Runtime").asText();
            	   String type = currentNode.path("Type").asText();
            	   String poster = currentNode.path("Poster").asText();
            	   String imdbVotes = currentNode.path("imdbVotes").asText();
            	   String imdbID = currentNode.path("imdbID").asText();
            	   String awards = currentNode.path("Awards").asText();
            	   
            	   List<String> writers = new ArrayList<>();
            	   for(String writer:currentNode.path("Writer").asText().split(",")){
            		   writers.add(writer.trim());
            	   }
            	   
            	   List<String> directors = new ArrayList<>();
            	   for(String director:currentNode.path("Director").asText().split(",")){
            		   directors.add(director.trim());
            	   }
            	   
            	   List<String> actors = new ArrayList<>();
            	   for(String actor:currentNode.path("Actors").asText().split(",")){
            		   actors.add(actor.trim());
            	   }
            	   
            	   List<String> genres = new ArrayList<>();
            	   for(String genre:currentNode.path("Genre").asText().split(",")){
            		   genres.add(genre.trim());
            	   }
            	   

            	   table.putItem(new Item()
            			   .withPrimaryKey("year", year, "title", title)
            			   .withString("plot", plot).withString("rated", rated)
            			   .withBoolean("response", response).withString("language", language)
            			   .withString("country",country).withString("metascore", metascore)
            			   .withString("imdbRating", imdbRating).withString("released", released)
            			   .withString("runtime", runtime).withString("type", type)
            			   .withString("poster", poster).withString("imdbVotes", imdbVotes)
            			   .withString("imdbID", imdbID).withString("awards", awards)
            			   .withList("writers", writers).withList("directors", directors)
            			   .withList("actors", actors).withList("genres", genres)
            			   );
            	   
            	   count++;
               }
               parser.close();
               System.out.println(objectSummary.getKey() + " :: " + count);
           }
        } while(result.isTruncated() == true ); 
        
        
        
        

//        JsonParser parser = new JsonFactory()
//            .createParser(new File("/Users/saurabhseth/Development/capstone/2016-1.json"));
//
//        JsonNode rootNode = new ObjectMapper().readTree(parser);
//        Iterator<JsonNode> iter = rootNode.path("ratings").elements();
//        ObjectNode currentNode;
//        while(iter.hasNext()){
//        	
//        	currentNode = (ObjectNode) iter.next();
//        	
//        	int year = currentNode.path("Year").asInt();
//        	String title = currentNode.path("Title").asText();
//        	
//        	try {
//        		table.putItem(new Item()
//        				.withPrimaryKey("year", year, "title", title)
//        				.withJSON("info", currentNode.toString()));
////        				.withJSON("rated", currentNode.path("Rated").toString())
////        				.withJSON("language", currentNode.path("Language").toString())
////        				.withJSON("country", currentNode.path("Country").toString())
////        				.withJSON("metascore", currentNode.path("Metascore").toString())
////        				.withJSON("imdbrating", currentNode.path("imdbRating").toString())
////        				.withJSON("director", currentNode.path("Director").toString())
////        				.withJSON("writer", currentNode.path("Writer").toString())
////        				.withJSON("released", currentNode.path("Released").toString())
////        				.withJSON("actors", currentNode.path("Actors").toString())
////        				.withJSON("genre", currentNode.path("Genre").toString())
////        				.withJSON("awards", currentNode.path("Awards").toString())
////        				.withJSON("imdbrating", currentNode.path("imdbRating").toString()));
////        		
////        		System.out.println("PutItem succeeded: " + year + " " + title);
//
//        	} catch (Exception e) {
//        		System.err.println("Unable to add movie: " + year + " " + title);
//        		System.err.println(e.getMessage());
//        		break;
//        	}
//        }
//        parser.close();
		
	}

}
