# Author: Eli Hughes

from app import db, Movie, Timestamp

# Unit test which primarily checks to see that db queries to the 'Movie' and 'Timestamp tables succeed 
# (connections remain stable) and receive the correct results.
def main():
    assert Movie.query.get(1).title == 'An Ideal Husband 1947', "Wrong Movie Result"
    print("Correct Movie")

    assert Timestamp.query.get(4866).subtitle == 'May I see you\r\n outside for a moment?\r\n', 'Wrong Timestamp Result'
    print("Correct Timestamp")

if __name__ == "__main__":
    for i in range(100):
        main()