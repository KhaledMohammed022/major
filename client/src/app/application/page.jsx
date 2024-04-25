'use client'
import React, { useState } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";

const Application = () => {
    const [accuracy, setAccuracy] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        const file = e.target.file.files[0]; // Get the file from the input element

        formData.append('file', file); // Append the file to FormData

        try {
            const response = await fetch('http://127.0.0.1:8080/train', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                    // Add any other necessary headers here
                },
                mode: 'no-cors', // Ensure CORS mode is enabled
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
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
                    <Label htmlFor="file" className="text-lg">Select Excel File</Label>
                    <Input type="file" id="file" name="file" accept=".xlsx" /> {/* Accept only .xlsx files */}
                    <Button type="submit" className="mt-4">Submit</Button>
                </form>
            </section>
            <section className="flex items-center justify-center p-10 flex-col">
                <h1 className="text-2xl font-bold">Output</h1>
                {accuracy && (
                    <div>
                        <p>Logistic Regression Accuracy: {accuracy.logistic_regression_accuracy}</p>
                        <p>Random Forest Accuracy: {accuracy.random_forest_accuracy}</p>
                    </div>
                )}
            </section>
        </>
    );
}

export default Application;
