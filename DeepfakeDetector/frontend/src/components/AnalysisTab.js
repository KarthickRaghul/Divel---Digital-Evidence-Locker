import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, AlertCircle, CheckCircle, Loader2 } from 'lucide-react'
import axios from 'axios'
import ResultsView from './ResultsView'

export default function AnalysisTab({ type, title, icon }) {
    const [file, setFile] = useState(null)
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [error, setError] = useState(null)
    const [preview, setPreview] = useState(null)

    const onDrop = useCallback(acceptedFiles => {
        const f = acceptedFiles[0]
        setFile(f)
        setResult(null)
        setError(null)

        // Create preview URL
        if (type !== 'audio') {
            const objectUrl = URL.createObjectURL(f)
            setPreview(objectUrl)
        }
    }, [type])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

    const handleAnalyze = async () => {
        if (!file && type !== 'url') return

        setLoading(true)
        setError(null)

        const formData = new FormData()
        formData.append('file', file)

        try {
            // Call FastAPI Backend
            // Assuming backend runs on 8000
            const endpoint = type === 'url' ? 'http://localhost:8000/analyze/url' : 'http://localhost:8000/analyze/upload'
            const res = await axios.post(endpoint, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })

            setResult(res.data)

        } catch (err) {
            console.error(err)
            setError("Analysis Failed. Ensure backend is running.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold flex items-center gap-2">
                    {icon} {title}
                </h2>
            </div>

            {!result ? (
                <div className="flex-1 flex flex-col items-center justify-center p-8">
                    <div
                        {...getRootProps()}
                        className={`w-full max-w-2xl text-center border-2 border-dashed rounded-xl p-10 cursor-pointer transition-all
                ${isDragActive ? 'border-primary bg-primary/10' : 'border-gray-700 hover:border-gray-500'}`}
                    >
                        <input {...getInputProps()} />
                        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                        <p className="text-xl mb-2 text-gray-300">
                            {file ? `Selected: ${file.name}` : "Drag & drop files here, or click to select"}
                        </p>
                        <p className="text-sm text-gray-500">Supports JPG, PNG, MP4, WAV, MP3</p>
                    </div>

                    {file && (
                        <button
                            onClick={handleAnalyze}
                            disabled={loading}
                            className="mt-8 bg-primary hover:bg-red-600 text-white px-8 py-3 rounded-full font-bold text-lg shadow-lg flex items-center gap-2 disabled:opacity-50"
                        >
                            {loading ? <Loader2 className="animate-spin" /> : "Start Forensic Analysis"}
                        </button>
                    )}

                    {loading && <div className="mt-4 text-gray-400 animate-pulse">Running Neural Networks...</div>}
                    {error && <div className="mt-4 text-red-500 bg-red-500/10 p-4 rounded-lg flex gap-2"><AlertCircle /> {error}</div>}
                </div>
            ) : (
                <ResultsView result={result} file={file} type={type} reset={() => setResult(null)} />
            )}
        </div>
    )
}
