"""CSV To Athlete HTML Script From Sample Code."""
import csv

def process_athlete_data(file_path):
   """Process Athlete Data."""

   # Sampple Code Variables
   records = []
   races = []           
   athlete_name = ""
   athlete_id = ""
   comments = ""

   # New Variables
   min_fin = 9999
   personal_record = None
   exp_years = []
   grades = []

   with open(file_path, newline='', encoding='utf-8') as file:
      reader = csv.reader(file)
      data = list(reader)

      athlete_name = data[0][0]
      athlete_id = data[1][0]
      print(f"The athlete id for {athlete_name} is {athlete_id}")

      for row in data[5:-1]:
         if row[2]:
            records.append({"year": row[2], "sr": row[3]})
            # keep track of years and grades for profile 
            exp_years.append (row[2])
            grades.append(row[3])
            # Check for PR for profile personal record
            if "PR" in row[3]:
               personal_record = row[3]
         else:
            races.append({
               "finish": row[1],
               "time": row[3],
               "meet": row[5],
               "url": row[6],
               "comments": row[7]
            })

      # Calculate Experience
      experience = len(exp_years)

      # Calculate Grade Level
      grade = grades[-1]
      grade_txt = "N/A"
      if grade == "9":
         grade_txt = "Freshman"
      if grade == "10":
         grade_txt = "Sophomore"
      if grade == "11":
         grade_txt = "Junior"
      if grade == "12":
         grade_txt = "Senior"

      # Calculate Top Place
      for index, place in enumerate(races):
         finish = place["finish"].strip()

         # fin_int = int(finish)
         # if fin_int < min_fin:
         #    min_fin = fin_int

      print(f"finish: {finish}")

   return {
      "name": athlete_name,
      "athlete_id": athlete_id,
      "season_records": records,
      "race_results": races,
      "comments": comments,
      "grade_txt": grade_txt,
      "experience": experience,
      "top_place": min_fin,
      "PR": personal_record,
   }    

def gen_athlete_page(data, outfile):
   """Generate Athlete Pages."""
   # template 
   # Start building the HTML structure
   html_content = f'''<!DOCTYPE html>
   <html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <!-- Get your own FontAwesome ID -->
      <script src="https://kit.fontawesome.com/YOUR_ID.js" crossorigin="anonymous"></script>

      <link rel = "stylesheet" href = "../css/reset.css">
      <link rel = "stylesheet" href = "../css/global.css">
      <link rel = "stylesheet" href = "../css/athlete.css">

      <title>{data["name"]}</title>
   </head>
   <body>
   <header>
      <div class="top-banner">
         <a href="../index.html">Ann Arbor Skyline XC</a>
      </div>
   </header>
   <nav class="navbar">
      <ul>
         <li><a href="#profile">Profile</a></li>
         <li><a href="#athlete-sr-table">Records</a></li>
         <li><a href="#athlete-result-table">Results</a></li>
         <li><a href="#gallery">Gallery</a></li>
      </ul>
   </nav>
   <main id = "main">
      <section id="profile">
      <!--Athlete would input headshot-->
      <div class="img-container">
         <img src="../images/profiles/{data["athlete_id"]}.jpg" alt="Athlete headshot" width="200"> 
      </div>
      <div>
         <h1>{data["name"]}</h1>
         <p class="profile_head">Grade: {data["grade_txt"]}</p>
         <p class="profile_head">Experience: {data["experience"]} years</p>
         <p class="profile_head">Top Place: {data["top_place"]}</p>
         <p class="profile_head">Personal Record: {data["PR"]}</p>
      </div>
      </section>
      <section id= "athlete-sr-table">
         <h2>Season Records (SR)</h2>
            <table>
                  <thead>
                     <tr>
                        <th> Year </th>
                        <th> Season Record (SR)</th>
                     </tr>
                  </thead>
                  <tbody>
                  '''
   
   for sr in data["season_records"]:
      sr_row = f'''
                     <tr>
                        <td>{sr["year"]}</td>
                        <td>{sr["sr"]}</td>
                     </tr>                  
               '''
      html_content += sr_row

   html_content += '''                   
                  </tbody>
            </table>
      </section>
      <section id="athlete-result-table">
            <h2>Race Results</h2>
            <table id="athlete-table">
                  <thead>
                        <tr>
                           <th>Race</th>
                           <th>Time</th>
                           <th>Place</th>
                           <th>Comments</th>
                        </tr>
                  </thead>
                  <tbody>
                  '''
   
   # add each race as a row into the race table 
   for race in data["race_results"]:
      race_row = f'''
                        <tr class="result-row">
                              <td>
                                 <a href="{race["url"]}">{race["meet"]}</a>
                              </td>
                              <td>{race["time"]}</td>
                              <td>{race["finish"]}</td>
                              <td>{race["comments"]}</td>
                        </tr>
                  '''
      html_content += race_row

   html_content += '''
                  </tbody>
            </table>
      </section>
      <section id = "gallery">
         <h2>Gallery</h2>
      </section>
   </main>
   <footer id="contact-us">
      <p>
         Skyline High School<br>
         <address>
            2552 North Maple Road<br>
            Ann Arbor, MI 48103<br><br>
               <a href = "https://sites.google.com/aaps.k12.mi.us/skylinecrosscountry2021/home">XC Skyline Page</a><br>
                  Follow us on Instagram <a href = "https://www.instagram.com/a2skylinexc/"><i class="fa-brands fa-instagram" aria-label="Instagram"></i>
               </a> 
   </footer>
   </body>
   </html>
   '''

   with open(outfile, 'w') as output:
      output.write(html_content)


def main():
   """Run the Script."""
   import os
   import glob

   # Define the folder path
   folder_path = 'mens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("mens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "mens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")


   # Define the folder path
   folder_path = 'womens_team/'
   # Get all csv files in the folder
   csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

   # Extract just the file names (without the full path)
   csv_file_names = [os.path.basename(file) for file in csv_files]

   # Output the list of CSV file names
   print(csv_file_names)
   for file in csv_file_names:

      # read data from file
      athlete_data = process_athlete_data("womens_team/"+file)
      # using data to generate templated athlete page
      gen_athlete_page(athlete_data, "womens_team/"+file.replace(".csv",".html"))

      # read data from file
      # athlete_data2 = process_athlete_data(filename2)
      # using data to generate templated athlete page
      # gen_athlete_page(athlete_data2, "enshu_kuan.html")

if __name__ == '__main__':
    main()
