from flask import Flask,render_template,request
import pickle
import numpy as np


popular_df=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity=pickle.load(open('similarity.pkl','rb'))
# Create an instance of the Flask application
app = Flask(__name__)

# Define a route and its associated function
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['Avg Ratings'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input=request.form.get('user_input')
    index = np.where(pt.index == user_input)[0]
    if index.size > 0:
        index = index[0]
        similar_books = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]

    data = []
    for i in similar_books:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)
    
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
