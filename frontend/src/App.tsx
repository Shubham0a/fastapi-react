import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/companies/';

function App() {
  const [companies, setCompanies] = useState([]);
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await axios.get(API_URL);
      setCompanies(response.data.companies);
    } catch (error) {
      console.error('Error fetching companies:', error);
    }
  };

  const addCompany = async () => {
    if (!name || !location) return;
    try {
      await axios.post(API_URL, { name, location });
      setName('');
      setLocation('');
      fetchCompanies();
    } catch (error) {
      console.error('Error adding company:', error);
    }
  };

  const deleteCompany = async (id) => {
    try {
      await axios.delete(`${API_URL}${id}`);
      fetchCompanies();
    } catch (error) {
      console.error('Error deleting company:', error);
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Company Management</h1>
      <div className="mb-4">
        <input
          type="text"
          placeholder="Company Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border p-2 mr-2"
        />
        <input
          type="text"
          placeholder="Location"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="border p-2 mr-2"
        />
        <button onClick={addCompany} className="bg-blue-500 text-white px-4 py-2">Add Company</button>
      </div>

      <div>
        {companies.length > 0 ? (
          <ul>
            {companies.map((company) => (
              <li key={company.id} className="mb-2">
                {company.name} - {company.location}
                <button onClick={() => deleteCompany(company.id)} className="bg-red-500 text-white px-2 py-1 ml-4">Delete</button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No companies found.</p>
        )}
      </div>
    </div>
  );
}

export default App;
