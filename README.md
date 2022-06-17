# Objective of code:
    This code converts textual data into array of numerical vectors, stores the numerical data and text data into 
      database and search for the entered text by converting it and matching its array of number.

## Libraries Used

#### 1. sqlite3: 
                    A library used to create and manage database and tables. 

#### 2. numpy: 
                    A library used to create and manage n-dimensional arrays. 

#### 3. io: 
                    A library that provides Python's main facilities for dealing with various types of I/O.. 

#### 4. time: 
                    A library used to manage and handel time and date related problems. 

#### 5. concurrent.futures: 
                    ThreadPoolExecutor to create and handle threads efficiently

#### 6. threading:
                    1.a Semaphore: To lock crucial parts of database

## Database Structure

### Database name:  vectorized.db
Contains 1 table with 3 column:
                                         
                                                      vectors   

                               |        text     |   numbers   |   sum_of_words  |
                               |-----------------|-------------|-----------------|
                               |        TEXT     |   BLOB      |    BLOB         |   
                               |                 |   (array)   |    (array)      |

## User defined functions:
1. create_table: Create a table named **vectors**.
2. delete_table: Delete the table.
3. convert_to_numbers: Take the raw list of strings and creates a list of numbers for each string by 
   using in-built function ord() and also creates a list conta
4. convert_to_string: Take the numbers list and convert them back to words using inbuilt function chr() and returns the 
   original string after joining using .join function 
5. insert: To insert multiple items into database using executemany.
6. fetch: To fetch all the data from database.
7. search: Takes a string to be searched in the database, converts it to numbers and run a search throughout the table 
   in database for matching items and return the data in string form after converting the numbers back to original 
   string along with its row id
8. threaded_search: 10 threads run concurrently to search the data from the database
## Working of Code
This code takes the batch of strings as inputs and convert them into numeric form, then store the list of numbers 
into **_vectors_** table in database named **_vectorized.db_** 
The fetch function fetches and print all the items from the **_vectors_** table and decode them back to their original string.
The search function takes argument that user needs to search in the database, converts it to numbers and run a search 
throughout the table in database for matching items and return the data in string form after converting the numbers 
back to original string along with its row id
Threaded_search is used to search through huge database more efficiently as it uses multiple-threads(currently 10) to 
divide the search into 10 equal parts and returning the original string along with row id after matching the array of 
list of numbers.