'use client';
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useToast } from "@/components/ui/use-toast"
import axios from 'axios';

const Application = () => {
    const [message, setMessage] = useState('');
    const [trainSamples, setTrainSamples] = useState('');
    const [testSamples, setTestSamples] = useState('');
    const [predictions, setPredictions] = useState('');
    const [accuracy, setAccuracy] = useState('');
    const [precision, setPrecision] = useState('');
    const [recall, setRecall] = useState('');
    const [f1Score, setF1Score] = useState('');
    const { toast } = useToast();

    const apiServerUrl = 'https://major-gjhv.onrender.com'; // Your API server URL

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        const file = e.target.file.files[0]; // Get the file from the input element

        formData.append('file', file); // Append the file to FormData

        try {
            const response = await axios.post(`${apiServerUrl}/api/upload`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // Change content type to multipart/form-data
                },
            });

            if (response.status !== 200) {
                toast({ description: "There was a problem with the fetch operation" });
                throw new Error('Network response was not ok');
            }
            if(response.status === 200 && response.data.message === "Dataset uploaded successfully"){
                toast({ description: "Dataset uploaded successfully" })
            }
            const data = response.data;
            setMessage(data.message);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handlePreprocess = async () => {
        try {
            const response = await axios.post(`${apiServerUrl}/api/preprocess`);

            if (response.status !== 200) {
                toast({ description: "There was a problem with the fetch operation" });
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
            setTrainSamples(data.train_samples);
            setTestSamples(data.test_samples);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handleTrainLR = async () => {
        try {
            const response = await axios.post(`${apiServerUrl}/api/train/lr`);

            if (response.status !== 200) {
                toast({ description: "There was a problem with the fetch operation" });
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
            setAccuracy(data.accuracy_score);
            setPrecision(data.precision_score);
            setRecall(data.recall_score);
            setF1Score(data.f1_score);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handleTrainDT = async () => {
        try {
            const response = await axios.post(`${apiServerUrl}/api/train/dt`);

            if (response.status !== 200) {
                toast({ description: "There was a problem with the fetch operation" });
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
            setAccuracy(data.accuracy_score);
            setPrecision(data.precision_score);
            setRecall(data.recall_score);
            setF1Score(data.f1_score);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handelTrainRF = async () => {
        try {
            const response = await axios.post(`${apiServerUrl}/api/train/rf`);

            if (response.status !== 200) {
                toast({ description: "There was a problem with the fetch operation" });
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
            setAccuracy(data.accuracy_score);
            setPrecision(data.precision_score);
            setRecall(data.recall_score);
            setF1Score(data.f1_score);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handlePredict = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        const file = document.getElementById('file').files[0]; // Get the file from the input element

        formData.append('file', file); // Append the file to FormData

        try {
            const response = await axios.post(`${apiServerUrl}/api/predict/lr`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // Change content type to multipart/form-data
                },
            });

            if (response.status !== 200) {
                toast({ description: "There was a problem with the fetch operation" });
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
            setPredictions(data.predictions);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    return (
        <>
            <section className="flex items-center justify-center p-20 flex-col">
                <h1 className="text-4xl font-bold">Application</h1>
            </section>
            <section className="flex flex-wrap justify-around">
                <section className='flex items-center justify-center p-15 '>    
                    <div className='flex items-center justify-center p-15 flex-col'>
                        <form onSubmit={handleSubmit} className="flex items-center justify-center p-2 flex-col">
                            <Label htmlFor="file" className="text-lg">Select CSV File</Label>
                            <Input type="file" id="file" name="file" accept=".csv" />
                            <Button type="submit" className="mt-4">Upload Dataset</Button>
                        </form>
                        <Button onClick={handlePreprocess} className="mt-4">Preprocess Dataset</Button>
                        <Button onClick={handleTrainLR} className="mt-4">Train Logistic Regression</Button>
                        <Button onClick={handleTrainDT} className="mt-4">Train Decision Tree</Button>
                        <Button onClick= {handelTrainRF} className="mt-4">Train Random Forest</Button>
                        <form onSubmit={handlePredict} className="flex items-center justify-center p-2 flex-col">
                            <Label htmlFor="file" className="text-lg">Select CSV File</Label>
                            <Input type="file" id="file" name="file" accept=".csv" />
                            <Button type="submit" className="mt-4">Upload Dataset for Prediction</Button>
                        </form>
                    </div>
                </section>
                <div>
                {trainSamples && (
                    <section className="flex items-center justify-center p-15 flex-col">
                        <h1 className="text-2xl font-bold">Training Samples</h1>
                        <p>Train Samples: {trainSamples}</p>
                        <p>Test Samples: {testSamples}</p>
                    </section>
                )}
                <br />
                {(accuracy || precision || recall || f1Score) && (
                    <section className="flex items-center justify-center p-15 flex-col">
                        <h1 className="text-2xl font-bold">Evaluation Metrics</h1>
                        <h3>{message}</h3>
                        <p>Accuracy: {accuracy}</p>
                        <p>Precision: {precision}</p>
                        <p>Recall: {recall}</p>
                        <p>F1 Score: {f1Score}</p>
                    </section>
                )}
                <br />
                {predictions && (
                    <section className="flex items-center justify-center p-15 flex-col">
                        <h1 className="text-2xl font-bold">Predictions</h1>
                        <p>Predictions: {predictions}</p>
                    </section>
                )}
                <br />
                <section className="flex items-center justify-center p-15 flex-col">
                    <h1 className="text-2xl font-bold">Output</h1>
                    <p>Message: {message}</p>
                </section>
                </div>
            </section>
        </>
    );
}

export default Application;
