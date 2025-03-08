from flask import Flask, request, render_template, redirect, url_for
from google.cloud import datastore

app = Flask(__name__)

# Initialize the Datastore client
datastore_client = datastore.Client()

# Company Info Kind
COMPANY_KIND = "Company_Info"

@app.route('/')
def index():
    """Home page that lists all companies."""
    query = datastore_client.query(kind=COMPANY_KIND)
    companies = list(query.fetch())
    return render_template('index.html', companies=companies)

@app.route('/create_company', methods=['GET', 'POST'])
def create_company():
    """Create a new company record."""
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        # Use the Ticker as the unique key
        key = datastore_client.key(COMPANY_KIND, data['Ticker'])
        entity = datastore.Entity(key=key)
        entity.update({
            'Ticker': data['Ticker'],
            'Company_Name': data['Company_Name'],
            'Industry': data['Industry']
        })
        datastore_client.put(entity)
        return redirect(url_for('index'))
    else:
        return render_template('create_company.html')

@app.route('/read_company/<ticker>')
def read_company(ticker):
    """Retrieve a single company record."""
    key = datastore_client.key(COMPANY_KIND, ticker)
    company = datastore_client.get(key)
    if not company:
        return "Company not found", 404
    return render_template('read_company.html', company=company)

@app.route('/update_company/<ticker>', methods=['GET', 'POST'])
def update_company(ticker):
    """Update a company record."""
    key = datastore_client.key(COMPANY_KIND, ticker)
    company = datastore_client.get(key)
    if not company:
        return "Company not found", 404

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        company['Company_Name'] = data['Company_Name']
        company['Industry'] = data['Industry']
        datastore_client.put(company)
        return redirect(url_for('read_company', ticker=ticker))
    else:
        return render_template('update_company.html', company=company)

@app.route('/delete_company/<ticker>')
def delete_company(ticker):
    """Delete a company record."""
    key = datastore_client.key(COMPANY_KIND, ticker)
    datastore_client.delete(key)
    return redirect(url_for('index'))

# --- TOPICS TABLE START ---

TOPICS_KIND = "Topics"

@app.route('/topics')
def topics_index():
    """List all topics."""
    query = datastore_client.query(kind=TOPICS_KIND)
    topics_list = list(query.fetch())
    return render_template('topics_index.html', topics=topics_list)

@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    """Create a new topic record."""
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        key = datastore_client.key(TOPICS_KIND)  # Auto-generated ID
        entity = datastore.Entity(key=key)
        entity.update({
            'Keyword': data['Keyword'],
            'Classification': data['Classification'],
            'Sector': data['Sector'],
            'Weight': float(data['Weight']) if data['Weight'] else 0.0
        })
        datastore_client.put(entity)
        return redirect(url_for('topics_index'))
    else:
        return render_template('create_topic.html')

@app.route('/read_topic/<int:topic_id>')
def read_topic(topic_id):
    """Retrieve a single topic record."""
    key = datastore_client.key(TOPICS_KIND, topic_id)
    topic = datastore_client.get(key)
    if not topic:
        return "Topic not found", 404
    return render_template('read_topic.html', topic=topic)

@app.route('/update_topic/<int:topic_id>', methods=['GET', 'POST'])
def update_topic(topic_id):
    """Update an existing topic."""
    key = datastore_client.key(TOPICS_KIND, topic_id)
    topic = datastore_client.get(key)
    if not topic:
        return "Topic not found", 404

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        topic['Keyword'] = data['Keyword']
        topic['Classification'] = data['Classification']
        topic['Sector'] = data['Sector']
        topic['Weight'] = float(data['Weight']) if data['Weight'] else 0.0
        datastore_client.put(topic)
        return redirect(url_for('read_topic', topic_id=topic_id))
    else:
        return render_template('update_topic.html', topic=topic)

@app.route('/delete_topic/<int:topic_id>')
def delete_topic(topic_id):
    """Delete a topic."""
    key = datastore_client.key(TOPICS_KIND, topic_id)
    datastore_client.delete(key)
    return redirect(url_for('topics_index'))

# --- TOPICS TABLE END ---

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
