from app import create_app

# Create Flask app
app = create_app()

# Start server only when file is executed directly
if __name__ == '__main__': 
    app.run(debug=True)

    
