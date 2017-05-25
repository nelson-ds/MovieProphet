package com.movies;

import com.amazonaws.AmazonClientException;
import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.profile.ProfileCredentialsProvider;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClient;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;

public class Connection {
	
	public static AmazonDynamoDBClient client;
	
	static{
		AWSCredentials credentials = null;
        try {
            credentials = new ProfileCredentialsProvider().getCredentials();
        } catch (Exception e) {
            throw new AmazonClientException(
                    "Cannot load the credentials from the credential profiles file. " +
                    "Please make sure that your credentials file is at the correct " +
                    "location (~/.aws/credentials), and is in valid format.",
                    e);
        }
        
        Region usWest2 = Region.getRegion(Regions.US_WEST_2);
        client = new AmazonDynamoDBClient(credentials);
        client.setRegion(usWest2);
	}
	
	// LOCAL CONNECTION
//	static{
//		AmazonDynamoDB client = AmazonDynamoDBClientBuilder.standard().withEndpointConfiguration(
//				new AwsClientBuilder.EndpointConfiguration("http://localhost:8000", "us-west-2"))
//				.build();
//
//		dynamoDB = new DynamoDB(client);
//	}

}
