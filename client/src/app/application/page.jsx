'use client';
import React from 'react'
import { Input } from '@/components/ui/input'
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"

const Application = () => {
    const handelSubmit = (e) => {
        e.preventDefault()
        const formData = new FormData()
        formData.append('file', e.target.file.files[0])
        fetch('http://localhost:8080/api/train', {
        method: 'POST',
        body: formData
        })
    }
  return (
    <>
    <section className="flex items-center justify-center p-20 flex-col">
        <h1 className="text-4xl font-bold">Application</h1>
    </section>
    <section className='flex items-center justify-center '>
        <form onSubmit={handelSubmit} className="flex items-center justify-center p-2 flex-col">
            <Label htmlFor="file" className="text-lg">Select File</Label>
            <Input type="file" id="file" name="file" />
            <Button type="submit" className="mt-4">Submit</Button>
        </form>
    </section>
    <section className="flex items-center justify-center p-10 flex-col">
        <h1 className="text-2xl font-bold">Output</h1>
    </section>
    </>
  )
}

export default Application