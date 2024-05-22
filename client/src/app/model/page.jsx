"use client";

import React, { useState, useRef } from "react";
import { Bar } from "react-chartjs-2";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast";
import axios from "axios";
import Chart from "chart.js/auto";
import { CategoryScale } from "chart.js";
import { motion } from "framer-motion";
import { LampContainer } from "@/components/ui/lamp";
import { Vortex } from "@/components/ui/vortex";
import { TypewriterEffect, TypewriterEffectSmooth } from "@/components/ui/typewriter-effect";

Chart.register(CategoryScale);

const Model = () => {
  const [message, setMessage] = useState("");
  const [trainSamples, setTrainSamples] = useState("");
  const [testSamples, setTestSamples] = useState("");
  const [predictions, setPredictions] = useState([]);
  const [accuracy, setAccuracy] = useState("");
  const [precision, setPrecision] = useState("");
  const [recall, setRecall] = useState("");
  const [f1Score, setF1Score] = useState("");
  const { toast } = useToast();

  const apiServerUrl = "https://major-gjhv.onrender.com"; // Your API server URL
  const [data, setData] = useState({});
  const chartRef = useRef(null);

  const options = {
    animation: {
      tension: {
        duration: 1000, // Animation duration in milliseconds
        easing: "easeInOutCubic", // Easing function for the animation
        from: 1, // Starting scale (1 means fully expanded)
        to: 0, // Ending scale (0 means fully collapsed)
        loop: true, // Repeat the animation
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    responsive: true,
  };

  const fetchData = async () => {
    try {
      const response = await axios.get(`${apiServerUrl}/api/metrics`);
      if (response.status !== 200) {
        throw new Error("Failed to fetch data");
      }

      const metrics = response.data;
      const labels = Object.keys(metrics);
      const accuracyData = labels.map((label) => metrics[label].accuracy);
      const precisionData = labels.map((label) => metrics[label].precision);
      const recallData = labels.map((label) => metrics[label].recall);
      const f1Data = labels.map((label) => metrics[label].f1);

      setData({
        labels: labels,
        datasets: [
          {
            label: "Accuracy",
            data: accuracyData,
            backgroundColor: "rgba(54, 162, 235, 0.6)", // Blue shade with transparency
            borderColor: "rgba(54, 162, 235, 1)", // Solid blue color
            borderWidth: 1,
          },
          {
            label: "Precision",
            data: precisionData,
            backgroundColor: "rgba(129, 178, 154, 0.6)", // Darker shade for Precision
            borderColor: "rgba(129, 178, 154, 1)",
            borderWidth: 1,
          },
          {
            label: "Recall",
            data: recallData,
            backgroundColor: "rgba(210, 215, 211, 0.6)", // Darker shade for Recall
            borderColor: "rgba(210, 215, 211, 1)",
            borderWidth: 1,
          },
          {
            label: "F1 Score",
            data: f1Data,
            backgroundColor: "rgba(249, 202, 36, 0.6)", // Darker shade for F1 Score
            borderColor: "rgba(249, 202, 36, 1)",
            borderWidth: 1,
          },
        ],
      });

      // Trigger animation after data is fetched
      if (chartRef.current) {
        chartRef.current.chartInstance.update();
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const file = e.target.file.files[0]; // Get the file from the input element

    formData.append("file", file); // Append the file to FormData

    try {
      const response = await axios.post(`${apiServerUrl}/api/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Change content type to multipart/form-data
        },
      });

      if (response.status !== 200) {
        toast({ description: "There was a problem with the fetch operation" });
        throw new Error("Network response was not ok");
      }
      if (response.status === 200 && response.data.message === "Dataset uploaded successfully") {
        toast({ description: "Dataset uploaded successfully" });
      }
      const data = response.data;
      setMessage(data.message);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  const handlePreprocess = async () => {
    try {
      const response = await axios.post(`${apiServerUrl}/api/preprocess`);

      if (response.status !== 200) {
        toast({ description: "There was a problem with the fetch operation" });
        throw new Error("Network response was not ok");
      }

      const data = response.data;
      setMessage(data.message);
      setTrainSamples(data.train_samples);
      setTestSamples(data.test_samples);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  const handleTrainLR = async () => {
    try {
      // Reset metrics to trigger typewriter effect
      setAccuracy("");
      setPrecision("");
      setRecall("");
      setF1Score("");

      const response = await axios.post(`${apiServerUrl}/api/train/lr`);

      if (response.status !== 200) {
        toast({ description: "There was a problem with the fetch operation" });
        throw new Error("Network response was not ok");
      }

      const data = response.data;
      setMessage(data.message);
      setAccuracy(data.accuracy_score);
      setPrecision(data.precision_score);
      setRecall(data.recall_score);
      setF1Score(data.f1_score);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  const handleTrainDT = async () => {
    try {
      // Reset metrics to trigger typewriter effect
      setAccuracy("");
      setPrecision("");
      setRecall("");
      setF1Score("");

      const response = await axios.post(`${apiServerUrl}/api/train/dt`);

      if (response.status !== 200) {
        toast({ description: "There was a problem with the fetch operation" });
        throw new Error("Network response was not ok");
      }

      const data = response.data;
      setMessage(data.message);
      setAccuracy(data.accuracy_score);
      setPrecision(data.precision_score);
      setRecall(data.recall_score);
      setF1Score(data.f1_score);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    const file = document.getElementById("predictFile").files[0]; // Get the file from the input element

    formData.append("file", file); // Append the file to FormData

    try {
      const response = await axios.post(`${apiServerUrl}/api/predict`, formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Change content type to multipart/form-data
        },
      });

      if (response.status !== 200) {
        toast({ description: "There was a problem with the fetch operation" });
        throw new Error("Network response was not ok");
      }

      const data = response.data;
      setMessage(data.message);
      setPredictions(data.predictions);
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  };

  return (
    <div className="relative z-10">
      <section className="flex items-center justify-center p-20 flex-col">
        <LampContainer>
          <motion.h1
            initial={{ opacity: 0.5, y: 100 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.3,
              duration: 0.8,
              ease: "easeInOut",
            }}
            className="mt-8 bg-gradient-to-br from-slate-300 to-slate-500 py-4 bg-clip-text text-center text-4xl font-medium tracking-tight text-transparent md:text-7xl"
          >
            ML Model
          </motion.h1>
        </LampContainer>
      </section>
      <Vortex
        backgroundColor="transparent"
        rangeY={800}
        particleCount={500}
        baseHue={120}
        className="flex items-center flex-col justify-center px-2 md:px-10 py-4 w-full h-full"
      >
        <section className="flex flex-wrap justify-around">
          <section className="flex items-center justify-center p-15">
            <div className="flex items-center justify-center p-15 flex-col">
              <form onSubmit={handleSubmit} className="flex items-center justify-center p-2 flex-col">
                <Label htmlFor="file" className="text-lg">
                  Select CSV File
                </Label>
                <Input type="file" id="file" name="file" accept=".csv" />
                <Button type="submit" className="mt-4">
                  Upload Dataset
                </Button>
              </form>
              <Button onClick={handlePreprocess} className="mt-4">
                Preprocess Dataset
              </Button>
              <Button onClick={handleTrainLR} className="mt-4">
                Train Logistic Regression
              </Button>
              <Button onClick={handleTrainDT} className="mt-4">
                Train Decision Tree
              </Button>
              <form onSubmit={handlePredict} className="flex items-center justify-center p-2 flex-col">
                <Label htmlFor="predictFile" className="text-lg">
                  Select CSV File for Prediction
                </Label>
                <Input type="file" id="predictFile" name="predictFile" accept=".csv" />
                <Button type="submit" className="mt-4">
                  Upload Dataset for Prediction
                </Button>
              </form>
            </div>
          </section>
          <div>
            {trainSamples && (
              <section className="flex items-center justify-center p-15 flex-col">
                <h1 className="text-2xl font-bold">Training Samples</h1>
                <p className="text-xl">Train Samples: {trainSamples}</p>
                <p className="text-xl">Test Samples: {testSamples}</p>
              </section>
            )}
            <br />
            {(accuracy || precision || recall || f1Score) && (
              <section className="flex items-center justify-center p-15 flex-col">
                <h1 className="text-2xl font-bold">Evaluation Metrics</h1>
                <h3>{message}</h3>
                <TypewriterEffect
                  words={[
                    { text: `Accuracy: `, className: "text-xl" },
                    { text:` ${accuracy}`, className: "text-xl text-blue-500 dark:text-blue-500",}
                  ]}
                  className="mb-1"
                />
                <TypewriterEffect
                  words={[
                    { text: `Precision: `, className: "text-xl" },
                    { text:` ${precision}`, className: "text-xl text-blue-500 dark:text-blue-500",}
                  ]}
                  className="mb-1"
                />
                <TypewriterEffect
                  words={[
                    { text: `Recall: `, className: "text-xl" },
                    { text:` ${recall}`, className: "text-xl text-blue-500 dark:text-blue-500",}
                  ]}
                  className="mb-1"
                />
                <TypewriterEffect
                  words={[
                    { text: `F1 Score: `, className: "text-xl" },
                    { text:` ${f1Score}`, className: "text-xl text-blue-500 dark:text-blue-500",}
                  ]}
                  className="mb-1"
                />
              </section>
            )}
            <br />
            {predictions.length > 0 && (
              <section className="flex items-center justify-center p-15 flex-col">
                <h1 className="text-2xl font-bold">Predictions</h1>
                {predictions.map((prediction, index) => (
                  <TypewriterEffectSmooth key={index} words={[{ text: prediction, className: "" }]} className="mb-2" />
                ))}
              </section>
            )}
            <br />
            <section className="flex items-center justify-center p-15 flex-col">
              <h1 className="text-2xl font-bold">Output</h1>
              <p>Message: {message}</p>
            </section>
          </div>
          <div>
            <h1 className="text-2xl font-bold">Model Comparison</h1>
            <br />
            {/* Your chart rendering */}
            {data.labels && (
              <Bar
                data={data}
                options={options}
                width={600}
                height={400}
                ref={chartRef}
              />            )}
            <br />
            {/* Button to fetch data and trigger animations */}
            <Button onClick={fetchData}>Fetch Data</Button>
          </div>
        </section>
      </Vortex>
    </div>
  );
};

export default Model;
