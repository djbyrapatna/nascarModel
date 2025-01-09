import React, { useState } from 'react';
import axios from 'axios';

const ModelForm = ({ onResult }) => {
  const [formData, setFormData] = useState({
    driverName: 'Chase Elliott',
    raceNumber: 20,
    year: 2024,
    modelDesc: '',
    cutoff: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
  console.log('API_BASE_URL:', API_BASE_URL); // Debugging log

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Basic validation
    if (!formData.driverName.trim()) {
      setError('Driver Name is required.');
      return;
    }
    if (isNaN(formData.raceNumber) || formData.raceNumber <= 0) {
      setError('Race Number must be a positive number.');
      return;
    }
    if (isNaN(formData.year) || formData.year < 1900 || formData.year > new Date().getFullYear()) {
      setError('Enter a valid Year.');
      return;
    }
    if (!formData.modelDesc.trim()) {
      setError('Model Description is required.');
      return;
    }
    if (isNaN(formData.cutoff) || formData.cutoff <= 0) {
      setError('Cutoff must be a positive number.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/query`, formData);
      onResult(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('An unexpected error occurred.');
      }
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Driver Name:</label>
        <input type="text" name="driverName" value={formData.driverName} onChange={handleChange} required />
      </div>
      <div>
        <label>Race Number:</label>
        <input type="number" name="raceNumber" value={formData.raceNumber} onChange={handleChange} required />
      </div>
      <div>
        <label>Year:</label>
        <input type="number" name="year" value={formData.year} onChange={handleChange} required />
      </div>
      <div>
        <label>Model Description:</label>
        <select name="modelDesc" value={formData.modelDesc} onChange={handleChange} required>
          <option value="">Select a Model</option>
          <option value="log">Logistic Regression</option>
          <option value="randomforest">Random Forest</option>
          <option value="xgBoost">XGBoost</option>
          <option value="svm">Support Vector Machine</option>
        </select>
      </div>
      <div>
        <label>Finishing Position:</label>
        <select name="cutoff" type="number" value={formData.cutoff} onChange={handleChange} required >
          <option value="">Select a Finishing Position</option>
          <option value="1">1</option>
          <option value="3">3</option>
          <option value="5">5</option>
          <option value="10">10</option>
          <option value="20">20</option>
        </select>
      </div>
      {error && <p className="error">{error}</p>}
      {loading ? <p>Loading...</p> : <button type="submit">Predict Probability</button>}
    </form>
  );
};

export default ModelForm;
