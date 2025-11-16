const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

const Reviews = require('./review');
const Dealerships = require('./dealership'); // Note: This uses the Dealership model from dealership.js

try {
  Reviews.deleteMany({}).then(() => {
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(() => {
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
} catch (error) {
  console.error("Initial data loading error:", error);
}

// Express route to home
app.get('/', async (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    // Ensure the ID is treated as a number since it's a numeric field in the schema
    const dealerId = parseInt(req.params.id);
    if (isNaN(dealerId)) {
      return res.status(400).json({ error: 'Invalid dealer ID' });
    }
    const documents = await Reviews.find({ dealership: dealerId });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching reviews for dealer' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    console.error("Error fetching all dealers:", error);
    res.status(500).json({ error: 'Error fetching all dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const stateParam = req.params.state;

    // FIX: Change the query field from 'st' (abbreviation) to 'state' (full name)
    const documents = await Dealerships.find({
      state: { $regex: new RegExp(`^${stateParam}$`, 'i') }
    });

    if (documents.length === 0) {
      return res.status(404).json({ error: `No dealerships found in state: ${stateParam}` });
    }

    res.json(documents);
  } catch (error) {
    console.error(`Error fetching dealers by state (${req.params.state}):`, error);
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const dealerId = parseInt(req.params.id);

    if (isNaN(dealerId)) {
      return res.status(400).json({ error: 'Invalid dealer ID format' });
    }

    const document = await Dealerships.findOne({ id: dealerId });

    if (!document) {
      return res.status(404).json({ error: `Dealership with ID ${dealerId} not found` });
    }

    res.json(document);
  } catch (error) {
    console.error(`Error fetching dealer by ID (${req.params.id}):`, error);
    res.status(500).json({ error: 'Error fetching dealership by ID' });
  }
});

// Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  const data = JSON.parse(req.body);

  // Find the maximum existing ID and increment it
  const documents = await Reviews.find().sort({ id: -1 });
  let new_id = 1; // Default ID if no documents exist
  if (documents.length > 0) {
    new_id = documents[0]['id'] + 1;
  }

  const review = new Reviews({
    id: new_id,
    name: data['name'],
    dealership: data['dealership'],
    review: data['review'],
    purchase: data['purchase'],
    purchase_date: data['purchase_date'],
    car_make: data['car_make'],
    car_model: data['car_model'],
    car_year: data['car_year'],
  });

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
