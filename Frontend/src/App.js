import React, { useEffect, useState } from "react";

const API_BASE_URL = "http://127.0.0.1:5000/get_data"

const countries = {
  me: "Middle East",
  sa: "Saudi Arabia",
  pk: "Pakistan",
  eg: "Egypt",
  gcc: "GCC Region",
};

function App() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [status, setStatus] = useState("pk"); // Default to valid country code
  const [selectedCountry, setSelectedCountry] = useState("pk");
  const [selectedDate, setSelectedDate] = useState(() =>
    new Date().toISOString().split("T")[0]
  );
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);


  const checkTime = (time) => {
    const hours = time.getHours();
    const minutes = time.getMinutes();
    const totalMinutes = hours * 60 + minutes;

    if (hours <= 11 && totalMinutes < 0) {
      setStatus("pk");
    } else if (hours >= 11 && totalMinutes < 0) {
      setStatus("me");
    } else if (hours >= 12 && totalMinutes < 20) {
      setStatus("sa");
    } else if (hours >= 12 && totalMinutes > 30) {
      setStatus("eg");
    } else {
      setStatus("pk");
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      setCurrentTime(now);
      checkTime(now);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Update selectedCountry when status changes
  useEffect(() => {
    if (countries[status]) {
      setSelectedCountry(status);
    }
  }, [status]);

  // Fetch data when country or date changes
  useEffect(() => {
    if (selectedCountry && selectedDate) {
      fetchData(selectedCountry, selectedDate);
    }
  }, [selectedCountry, selectedDate]);

  const fetchData = async (countryCode, date) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(API_BASE_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          country_code: countryCode,
          date: date,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-6">
      <h1 className="text-2xl md:text-3xl font-bold text-gray-800 mb-6 text-center">
        Platform Data Overview
      </h1>

      <p className="text-gray-700 mb-4">{currentTime.toLocaleString()}</p>

      {/* Country Dropdown */}
      <div className="flex flex-col md:flex-row gap-4 mb-6">
        <select
          className="px-4 py-2 border border-gray-300 rounded-lg shadow-sm"
          value={selectedCountry}
          onChange={(e) => setSelectedCountry(e.target.value)}
        >
          {Object.entries(countries).map(([code, name]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>

        {/* Date Picker */}
        <input
          type="date"
          className="px-4 py-2 border border-gray-300 rounded-lg shadow-sm"
          placeholder="dd/mm/yyyy"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
        />

      </div>

      {/* Loading & Error Messages */}
      {loading && (
        <p className="text-lg font-semibold text-blue-600">Loading data...</p>
      )}
      {error && (
        <p className="text-lg font-semibold text-red-600">{error}</p>
      )}

      {/* Summary Cards */}
      {data && (
        <div className="flex flex-col md:flex-row gap-4 w-full max-w-md">
          <div className="bg-white shadow-md rounded-lg p-4 text-center flex-1">
            <h3 className="text-lg font-semibold text-gray-600">Actual Platforms</h3>
            <p className="text-xl font-bold text-blue-500">
              {data["Actual Platforms"]}
            </p>
          </div>
          <div className="bg-white shadow-md rounded-lg p-4 text-center flex-1">
            <h3 className="text-lg font-semibold text-gray-600">
              Today's Platform Number
            </h3>
            <p className="text-xl font-bold text-blue-500">
              {data["Todays Platform Number"]}
            </p>
          </div>
        </div>
      )}

      {/* Table */}
      {data?.result && (
        <div className="overflow-x-auto w-full max-w-3xl mt-6">
          <table className="min-w-full bg-white border border-gray-300 rounded-lg shadow-md">
            <thead>
              <tr className="bg-blue-500 text-white">
                <th className="py-3 px-4 border">Platform Name</th>
                <th className="py-3 px-4 border">Available</th>
                <th className="py-3 px-4 border">Count</th>
              </tr>
            </thead>
            <tbody>
              {data.result.map((item, index) => {
                const platformName = Object.keys(item)[0];
                return (
                  <tr key={index} className="text-center border-b">
                    <td className="py-3 px-4 border font-semibold">
                      {platformName}
                    </td>
                    <td className="py-3 px-4 border">
                      {item[platformName] ? "✅ Yes" : "❌ No"}
                    </td>
                    <td className="py-3 px-4 border">{item.count}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
