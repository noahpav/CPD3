import os
import csv

# Paths to the team folders, events folder, images folder
mens_team_folder = './mens_team'
womens_team_folder = './womens_team'
events_folder = './meets'
images_folder = './images/profiles'
html_file_path = './index.html'

# Base URL for images relative to the HTML file location
image_base_path = '/images/profiles/'

# HTML template as a multi-line string
html_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Organization Home Page</title>
    <link rel="stylesheet" href="css/reset.css" />
    <link rel="stylesheet" href="css/global.css" />
    <link rel="stylesheet" href="css/index.css" />
  </head>
  <body>
    <header>
      <div class="top-banner">
        <a href="index.html">Ann Arbor Skyline XC</a>
      </div>
    </header>
    <nav class="navbar">
      <ul>
        <li><a href="#teams-section">Teams</a></li>
        <li><a href="#calandar">Calandar</a></li>
        <li><a href="#gallery">Gallery</a></li>
        <li><a href="#contact-us">Contact</a></li>
      </ul>
    </nav>
    <main class="content-section">
      <!-- Teams Section -->
      <section id="teams-section" class="teams-section">
        <h1>Teams</h1>

        <div class="team-container">
          <!-- Mens Team -->
          <div class="team">
            <h2>Mens</h2>
            <table>
              <th>
                Athlete Name
              </th>
              <tr>
                {mens_team_athletes}
              </tr>
            </table>
          </div>

          <!-- Womens Team -->
          <div class="team">
            <h2>Womens</h2>
            <table>
              <th>
                Athlete Name
              </th>
              <tr>
                {womens_team_athletes}
              </tr>
            </table>
          </div>
        </div>
      </section>

      <!-- Events Section -->
      <section id="calandar" class="content">
        <h2>Season Calendar</h2>
        <ul>
            <li>August 18, 2023 - <a href=https://www.athletic.net/CrossCountry/meet/221431/info>Lamplighter Invite</a></li>
            <li>September 9, 2023 - <a href=https://www.athletic.net/CrossCountry/meet/221738/info>Bret Clemets Bath Invitational</a></li>
        </ul>
      </section>

      <!-- Photo Gallery Section -->
      <section id="gallery"  class="gallery">
        <h2>Photo Gallery</h2>
        <div class="photo-grid">
        {gallery_section}
        </div>
      </section>
    </main>

    <!-- Contact Section -->
    <footer>
      <div id="contact-us" class="contact">
        <h2>Contact Us</h2>
        <p>Email: contact@xcountry.org</p>
        <p>Phone: (123) 456-7890</p>
        <p>Address: 123 XCountry Lane, City, State, ZIP</p>
      </div>
    </footer>
  </body>
</html>
"""

# Function to get athlete names from CSV files, sorted alphabetically
def get_athlete_names(folder):
    athlete_names = []
    for filename in sorted(os.listdir(folder)):  # Use sorted to keep names in alphabetical order
        if filename.endswith('.csv'):
            with open(os.path.join(folder, filename), 'r') as csv_file:
                reader = csv.reader(csv_file)
                athlete_name = next(reader)[0]  # Get the first line, first column
                html_file = filename.replace('.csv', '.html')  # Convert CSV filename to HTML filename
                athlete_names.append((athlete_name, html_file))
    return athlete_names

# Function to generate HTML for the athlete list with links to individual pages
def generate_athlete_list_html(athlete_names, folder):
    athlete_html = ""
    for name, html_file in athlete_names:
        athlete_html += f"<tr><td><a href='{folder}/{html_file}'>{name}</a></td></tr>\n"
    return athlete_html

# Function to generate the gallery HTML
def generate_gallery_html(images_folder):
    gallery_html = ""
    for image_file in os.listdir(images_folder):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image_path = f"{image_base_path}{image_file}"
            gallery_html += f"""
            <img src="{image_path}" alt="Photo" class="gallery-image" style="width: 150px; height: auto; margin: 5px;">
            """
    return gallery_html

# Get athlete names from men's and women's teams
mens_team_names = get_athlete_names(mens_team_folder)
womens_team_names = get_athlete_names(womens_team_folder)

# Generate the athlete list HTML with links to individual pages
mens_team_html = generate_athlete_list_html(mens_team_names, mens_team_folder)
womens_team_html = generate_athlete_list_html(womens_team_names, womens_team_folder)

# Generate the gallery HTML
gallery_html = generate_gallery_html(images_folder)

# Replace placeholders in the template with generated content in one step
html_output = html_template.format(
    mens_team_athletes=mens_team_html,
    womens_team_athletes=womens_team_html,
    gallery_section=gallery_html
)

# Save the output to the index.html file
with open(html_file_path, 'w') as output_file:
    output_file.write(html_output)

print("index.html page has been successfully generated.")
