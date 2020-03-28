# Add our dependencies.
import csv
import os

class PyPoll:

    # Define initial dict of counties
    counties = {}

    # Candidate options and candidate votes.
    candidate_votes = {}

    # Initialize a total vote counter.
    total_votes = 0

    # Assign a variable to load a file from a path.
    file_to_read = os.path.join("Resources/election_results.csv")
    # Assign a variable to save the file to a path.
    file_to_save = os.path.join("analysis", "election_analysis.txt")

    def calculate_percent_vote(self,county_vote):
        return (county_vote / self.total_votes) * 100

    def format_county_vote(self,county_name,county_votes):
        return (
            f"{county_name.title()}: "
            f"{self.calculate_percent_vote(county_votes):.1f}% "
            f"({county_votes:,})\n"
        )
    def format_line_divide(self,with_newline=True):
        if with_newline:
            return f"-------------------------\n"
        return f"-------------------------"
    def format_winning_candidate(self,winning_candidate,winning_count,winning_percentage):
        return (
            f"Winner: {winning_candidate}\n"
            f"Winning Vote Count: {winning_count:,}\n"
            f"Winning Percentage: {winning_percentage:.1f}%\n")
    def format_title(self,title):
        return (f"{title}\n")
    def format_total_votes(self):
        return (f"Total Votes: {self.total_votes:,}\n")

    def print_output_file(self):
        with open(self.file_to_save) as fh_saved:
            print(fh_saved.read())

    def write_winning_candidate(self):
        # Save the results to our text file.
        with open(self.file_to_save, "w") as txt_file:
            # Save the final vote count to the text file.
            txt_file.write(self.format_title("\nElection Results"))
            txt_file.write(self.format_line_divide())
            txt_file.write(self.format_total_votes())
            txt_file.write(self.format_line_divide())
            txt_file.write(self.format_title("\nCounty Votes:"))

            max_votes = 0
            largest_county = ""
            for county_name in self.counties.keys():
                format_country = self.format_county_vote(county_name, self.counties[county_name]['count'])
                txt_file.write(format_country)
                if max_votes <  self.counties[county_name]['count']:
                    max_votes =  self.counties[county_name]['count']
                    largest_county = county_name
            
            txt_file.write("\n")
            txt_file.write(self.format_line_divide())
            txt_file.write(self.format_title("Largest County Turnout: " + largest_county))
            txt_file.write(self.format_line_divide())

            # Track the winning candidate, vote count, and percentage.
            winning_candidate = ""
            winning_count = 0
            winning_percentage = 0
            for candidate in self.candidate_votes:
                # Retrieve vote count and percentage.
                votes = self.candidate_votes[candidate]
                vote_percentage = self.calculate_percent_vote(votes)
                candidate_results = (f"{candidate}: {vote_percentage:.1f}% ({votes:,})\n")

                #  Save the candidate results to our text file.
                txt_file.write(candidate_results)
                # Determine winning vote count, winning percentage, and winning candidate.
                if (votes > winning_count) and (vote_percentage > winning_percentage):
                    winning_count = votes
                    winning_candidate = candidate
                    winning_percentage = vote_percentage
            txt_file.write(self.format_line_divide())
            winning_candidate_summary = self.format_winning_candidate(winning_candidate,winning_count,winning_percentage)
            # Save the winning candidate's results to the text file.
            txt_file.write(winning_candidate_summary)
            txt_file.write(self.format_line_divide(False))
            
    def read_election_row(self,row):
        # Add to the total vote count.
        self.total_votes += 1

        # Get the county name from each row.
        county_name = row[1]
        # If the county does not exist in the counties dict
        if county_name not in self.counties:
            # Initialize a county dict and a county for that county
            self.counties[county_name] = {}
            self.counties[county_name]['count'] = 0

        # Get the candidate name from each row.
        candidate_name = row[2]
        # If the candidate does not exist in the county dict then initialize.
        if candidate_name not in self.counties[county_name]:
            self.counties[county_name][candidate_name] = 0

        # Increase the county vote for that candidate and total county vote
        self.counties[county_name][candidate_name] = self.counties[county_name][candidate_name] + 1
        self.counties[county_name]['count'] = self.counties[county_name]['count'] + 1

        # If the candidate does not match any existing candidate, add the candidate list.
        if candidate_name not in self.candidate_votes:
            # And begin tracking that candidate's voter count.
            self.candidate_votes[candidate_name] = 0
        # Add a vote to that candidate's count.
        self.candidate_votes[candidate_name] += 1

    def read_election_file(self):
        # Open the election results and read the file.
        with open(self.file_to_read) as election_data:
            file_reader = csv.reader(election_data)
            # Read the header row.
            headers = next(file_reader)
            # Print each row in the CSV file.
            for row in file_reader:
                self.read_election_row(row)

    # Main starting function for the PyPoll Challenge
    def pypoll(self):
        # First read the election data
        self.read_election_file()
        # Then write the results to file
        self.write_winning_candidate()
        # Finally print the output file to console.
        self.print_output_file()

def main():
    # Instantiate object
    p = PyPoll()
    # Run challenge
    p.pypoll()

if __name__ == '__main__':
    main()
