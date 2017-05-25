package com.movies;

import java.util.HashMap;
import java.util.Iterator;

import com.amazonaws.client.builder.AwsClientBuilder;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.dynamodbv2.document.ItemCollection;
import com.amazonaws.services.dynamodbv2.document.QueryOutcome;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.document.spec.QuerySpec;

public class MoviesQuery {

	public static void main(String[] args) throws Exception {

        Table table = new DynamoDB(Connection.client).getTable("MovieRatings");

        HashMap<String, String> nameMap = new HashMap<String, String>();
        nameMap.put("#yr", "year");

        HashMap<String, Object> valueMap = new HashMap<String, Object>();
        valueMap.put(":yyyy", 2016);

        QuerySpec querySpec = new QuerySpec()
            .withKeyConditionExpression("#yr = :yyyy")
            .withNameMap(nameMap)
            .withValueMap(valueMap);

        ItemCollection<QueryOutcome> items = null;
        Iterator<Item> iterator = null;
        Item item = null;

        try {
            System.out.println("Movies from 2016");
            items = table.query(querySpec);

            iterator = items.iterator();
            int count = 0;
            while (iterator.hasNext()) {
                item = iterator.next();
                count++;
                
            }
            System.out.println(count);

        } catch (Exception e) {
            System.err.println("Unable to query movies from 2016");
            System.err.println(e.getMessage());
        }

        valueMap.put(":yyyy", 2016);
        valueMap.put(":letter1", "A");
        valueMap.put(":letter2", "L");

        querySpec
                .withProjectionExpression(
                        "#yr, title, info.Genre, info.Actors")
                .withKeyConditionExpression(
                        "#yr = :yyyy and title between :letter1 and :letter2")
                .withNameMap(nameMap).withValueMap(valueMap);

        try {
            System.out
                    .println("Movies from 2016 - titles A-L, with genres and lead actor");
            items = table.query(querySpec);

            iterator = items.iterator();
            while (iterator.hasNext()) {
                item = iterator.next();
                System.out.println(item.getNumber("year") + ": "
                        + item.getString("title") + " " + item.getMap("info"));
            }

        } catch (Exception e) {
            System.err.println("Unable to query movies from 2016:");
            System.err.println(e.getMessage());
        }
    }

}
