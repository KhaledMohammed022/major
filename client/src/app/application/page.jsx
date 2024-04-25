'use client'
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import axios from 'axios';

const Application = () => {
    const [accuracy, setAccuracy] = useState(null);

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
            setAccuracy(data);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }

    return (
        <>
            <section className="flex items-center justify-center p-20 flex-col">
                <h1 className="text-4xl font-bold">Application</h1>
            </section>
            <section className='flex items-center justify-center '>
                <form onSubmit={handleSubmit} className="flex items-center justify-center p-2 flex-col">
                    <Label htmlFor="file" className="text-lg">Select CSV File</Label> {/* Update label */}
                    <Input type="file" id="file" name="file" accept=".csv" /> {/* Accept only .csv files */}
                    <Button type="submit" className="mt-4">Submit</Button>
                </form>
            </section>
            <section className="flex items-center justify-center p-10 flex-col">
                <h1 className="text-2xl font-bold">Output</h1>
                {accuracy && (
                    <div>
                        <p>Message: {accuracy.message}</p>
                        <p>Train Samples: {accuracy.train_samples}</p>
                        <p>Test Samples: {accuracy.test_samples}</p>
                        <p>Logistic Regression Accuracy: {accuracy.lr_accuracy}</p>
                        <p>Decision Tree Accuracy: {accuracy.dt_accuracy}</p>
                    </div>
                )}
            </section>
        </>
    );
}

export default Application;
