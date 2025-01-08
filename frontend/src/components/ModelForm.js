// ModelForm.js
import React, { useState } from 'react';
import axios from 'axios';

const ModelForm = ({ onResult }) => {
  const [formData, setFormData] = useState({
    driverName: '',
    raceNumber: '',
    year: '',
    modelDesc: '',
    cutoff: ''
  });
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post(`${process.env.REACT_APP_API_BASE_URL}/query`, formData);
      onResult(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('An unexpected error occurred.');
      }
    }
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
        <input type="text" name="modelDesc" value={formData.modelDesc} onChange={handleChange} required />
      </div>
      <div>
        <label>Cutoff:</label>
        <input type="number" name="cutoff" value={formData.cutoff} onChange={handleChange} required />
      </div>
      {error && <p className="error">{error}</p>}
      <button type="submit">Predict Probability</button>
    </form>
  );
};

export default ModelForm;
