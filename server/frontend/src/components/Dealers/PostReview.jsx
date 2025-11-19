import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Dealers.css";
import "../assets/style.css";
import Header from "../Header/Header";

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);

  const params = useParams();
  const id = params.id;

  const curr_url = window.location.href;
  const root_url = curr_url.substring(0, curr_url.indexOf("postreview"));

  const dealer_url = root_url + `djangoapp/dealer/${id}`;
  const review_url = root_url + `djangoapp/add_review`;
  const carmodels_url = root_url + `djangoapp/get_cars`;

  // Fetch dealer info
  const get_dealer = async () => {
    try {
      const res = await fetch(dealer_url);
      const retobj = await res.json();
      if (retobj.status === 200) setDealer(retobj.dealer);
    } catch (err) {
      console.log("Error fetching dealer:", err);
    }
  };

  // Fetch car models
  const get_cars = async () => {
    try {
      const res = await fetch(carmodels_url);
      const retobj = await res.json();
      console.log("Car models fetched:", retobj); // debug
      if (retobj.CarModels) setCarmodels(retobj.CarModels);
    } catch (err) {
      console.log("Error fetching car models:", err);
    }
  };

  // Post review
  const postreview = async () => {
    let name =
      sessionStorage.getItem("firstname") +
      " " +
      sessionStorage.getItem("lastname");

    if (name.includes("null")) {
      name = sessionStorage.getItem("username");
    }

    if (!model || review.trim() === "" || date === "" || year === "") {
      alert("All details are mandatory");
      return;
    }

    const [make_chosen, model_chosen] = model.split(" ");

    const jsoninput = JSON.stringify({
      name,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: make_chosen,
      car_model: model_chosen,
      car_year: year,
    });

    const res = await fetch(review_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsoninput,
    });

    const json = await res.json();
    if (json.status === 200) {
      window.location.href = window.location.origin + "/dealer/" + id;
    }
  };

  useEffect(() => {
    get_dealer();
    get_cars();
  }, []);

  return (
    <div>
      <Header />
      <div style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name}</h1>

        <textarea
          cols="50"
          rows="7"
          onChange={(e) => setReview(e.target.value)}
          placeholder="Write your review..."
        />

        <div className="input_field">
          Purchase Date{" "}
          <input type="date" onChange={(e) => setDate(e.target.value)} />
        </div>

        <div className="input_field">
          Car Make{" "}
          {carmodels.length > 0 ? (
            <select
              name="cars"
              id="cars"
              defaultValue=""
              onChange={(e) => setModel(e.target.value)}
            >
              <option value="" disabled>
                Choose Car Make and Model
              </option>
              {carmodels.map((carmodel, idx) => (
                <option
                  key={idx}
                  value={carmodel.CarMake + " " + carmodel.CarModel}
                >
                  {carmodel.CarMake} {carmodel.CarModel}
                </option>
              ))}
            </select>
          ) : (
            <p>Loading car models...</p>
          )}
        </div>

        <div className="input_field">
          Car Year{" "}
          <input
            type="number"
            onChange={(e) => setYear(e.target.value)}
            min={2015}
            max={new Date().getFullYear()}
          />
        </div>

        <div>
          <button className="postreview" onClick={postreview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
