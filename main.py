from website import create_app, views, models

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
