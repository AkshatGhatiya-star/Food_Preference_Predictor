import pandas as pd
import random

# --- Expanded Configuration for a Richer Indian Context ---

# Expanded list of Indian cities and their states
indian_cities = {
    'Mumbai': 'Maharashtra', 'Delhi': 'Delhi', 'Bangalore': 'Karnataka', 'Chennai': 'Tamil Nadu',
    'Kolkata': 'West Bengal', 'Hyderabad': 'Telangana', 'Pune': 'Maharashtra', 'Ahmedabad': 'Gujarat',
    'Jaipur': 'Rajasthan', 'Lucknow': 'Uttar Pradesh', 'Bhopal': 'Madhya Pradesh', 'Chandigarh': 'Chandigarh',
    'Indore': 'Madhya Pradesh', 'Patna': 'Bihar', 'Agra': 'Uttar Pradesh', 'Varanasi': 'Uttar Pradesh',
    'Srinagar': 'Jammu and Kashmir', 'Kochi': 'Kerala', 'Visakhapatnam': 'Andhra Pradesh',
    'Guwahati': 'Assam', 'Nagpur': 'Maharashtra', 'Ludhiana': 'Punjab', 'Surat': 'Gujarat'
}

seasons = ['Winter', 'Summer', 'Monsoon', 'Autumn']
income_levels = ['Low', 'Medium', 'High']
stress_levels = ['Low', 'Medium', 'High']
work_life_balances = ['Poor', 'Average', 'Good', 'Excellent']
contexts = ['Urban', 'Rural']

# Massively expanded list of Indian recommended foods for more variety
recommended_foods = [
    'Roti with Dal Tadka', 'Vegetable Pulao', 'Paneer Butter Masala', 'Aloo Gobi', 'Chole Bhature',
    'Masala Dosa', 'Idli Sambar', 'Chicken Biryani', 'Palak Paneer', 'Dal Makhani', 'Rajma Chawal',
    'Goan Fish Curry with Rice', 'Vegetable Korma', 'Upma', 'Poha', 'Lemon Rice', 'Curd Rice',
    'Mixed Vegetable Curry', 'Bhindi Masala', 'Baingan Bharta', 'Tandoori Chicken Salad',
    'Moong Dal Khichdi', 'Shahi Paneer', 'Mutton Rogan Josh', 'Sarson ka Saag with Makki di Roti',
    'Dhokla', 'Khandvi', 'Thepla', 'Vada Pav', 'Pav Bhaji', 'Misal Pav', 'Hyderabadi Dum Biryani',
    'Litti Chokha', 'Bengali Fish Fry', 'Kosha Mangsho', 'Aloo Posto', 'Chettinad Chicken',
    'Avial', 'Kerala Prawn Curry', 'Bisi Bele Bath', 'Mysore Pak', 'Gajar ka Halwa', 'Gulab Jamun',
    'Rasmalai', 'Jalebi with Rabri', 'Sprout Salad', 'Oats Idli', 'Quinoa Upma', 'Egg Curry',
    'Soya Chaap Masala', 'Kathal (Jackfruit) Biryani', 'Mushroom Matar', 'Kadai Paneer'
]

def generate_indian_dataset(num_records=2000): # Increased to 2000
    """Generates a large and diverse dataset with an Indian context."""
    data = []
    for _ in range(num_records):
        city, state = random.choice(list(indian_cities.items()))
        record = {
            'Weight': random.randint(50, 100),
            'City': city,
            'State': state,
            'Temperature': random.randint(10, 42), # Adjusted temperature range
            'Season': random.choice(seasons),
            'Income_Level': random.choice(income_levels),
            'Stress_Level': random.choice(stress_levels),
            'Sleep_Hours': random.randint(4, 9),
            'Work_Life_Balance': random.choice(work_life_balances),
            'Context': random.choice(contexts),
            'Recommended_Food': random.choice(recommended_foods)
        }
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating new, large Indian food recommendation database...")
    
    # We will generate 2000 records
    indian_df = generate_indian_dataset(2000)
    
    output_filename = 'indian_food_recs_database.csv'
    indian_df.to_csv(output_filename, index=False)
    
    print(f"✅ Successfully created '{output_filename}' with {len(indian_df)} records.")