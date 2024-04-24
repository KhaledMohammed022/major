import React from 'react';
import { Input } from '@/components/ui/input';
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import axios from 'axios';

const Application = () => {
    const handelSubmit = (e) => {
        e.preventDefault();
        const formData = new FormData();
        const file = e.target.file.files[0]; // Get the file from the input element
        const reader = new FileReader();

        reader.onload = (event) => {
            const result = event.target.result;
            const workbook = XLSX.read(result, { type: 'binary' }); // Read the Excel file
            const firstSheet = workbook.Sheets[workbook.SheetNames[0]]; // Get the first sheet
            const csv = XLSX.utils.sheet_to_csv(firstSheet); // Convert the sheet to CSV format

            // Create a Blob object from the CSV data and append it to the FormData object
            const blob = new Blob([csv], { type: 'text/csv' });
            formData.append('file', blob, file.name);

            // Send the FormData object with Axios POST request
            axios.post('http://localhost:8080/train', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data' // Set the content type to multipart/form-data
                }
            })
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        };

        reader.readAsBinaryString(file);
    }

    return (
        <>
            <section className="flex items-center justify-center p-20 flex-col">
                <h1 className="text-4xl font-bold">Application</h1>
            </section>
            <section className='flex items-center justify-center '>
                <form onSubmit={handelSubmit} className="flex items-center justify-center p-2 flex-col">
                    <Label htmlFor="file" className="text-lg">Select Excel File</Label>
                    <Input type="file" id="file" name="file" accept=".xlsx" /> {/* Accept only .xlsx files */}
                    <Button type="submit" className="mt-4">Submit</Button>
                </form>
            </section>
            <section className="flex items-center justify-center p-10 flex-col">
                <h1 className="text-2xl font-bold">Output</h1>
            </section>
        </>
    );
}

export default Application;
