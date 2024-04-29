'use client'
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import axios from 'axios';

const Application = () => {
    const [message, setMessage] = useState('');
    const [trainSamples, setTrainSamples] = useState('');
    const [testSamples, setTestSamples] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        const file = e.target.file.files[0]; // Get the file from the input element

        formData.append('file', file); // Append the file to FormData

        try {
            const response = await axios.post('http://127.0.0.1:8080/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data', // Change content type to multipart/form-data
                },
            });

            if (response.status !== 200) {
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handlePreprocess = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8080/api/preprocess');

            if (response.status !== 200) {
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
            const response = await axios.post('http://127.0.0.1:8080/api/train/lr');

            if (response.status !== 200) {
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    const handleTrainDT = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8080/api/train/dt');

            if (response.status !== 200) {
                throw new Error('Network response was not ok');
            }

            const data = response.data;
            setMessage(data.message);
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
                <form onSubmit={handleSubmit} className="flex items-center justify-center p-2 flex-col">
                    <Label htmlFor="file" className="text-lg">Select CSV File</Label>
                    <Input type="file" id="file" name="file" accept=".csv" />
                    <Button type="submit" className="mt-4">Upload Dataset</Button>
                    <Button onClick={handlePreprocess} className="mt-4">Preprocess Dataset</Button>
                    <Button onClick={handleTrainLR} className="mt-4">Train Logistic Regression</Button>
                    <Button onClick={handleTrainDT} className="mt-4">Train Decision Tree</Button>
                </form>
            </section>
            <section className="flex items-center justify-center p-15 flex-col">
                <h1 className="text-2xl font-bold">Output</h1>
                <p>Message: {message}</p>
                <p>Train Samples: {trainSamples}</p>
                <p>Test Samples: {testSamples}</p>
            </section>
            </section>
        </>
    );
}

export default Application;

