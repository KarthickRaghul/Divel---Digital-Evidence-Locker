import React, { useState, useCallback } from 'react';
import { Layout } from '@/components/layout/Layout';
import { useDropzone } from 'react-dropzone';
import { Upload, File, AlertTriangle, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';
import Lottie from 'lottie-react';
import faceRecognitionData from '../assets/face recognition.json';

// Types for the analysis result
interface AnalysisResult {
    filename: string;
    type: string;
    visual_score: number;
    audio_score: number;
    final_score: number;
    verdict: string;
    details: any;
}

const DeepfakeDetector: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [preview, setPreview] = useState<string | null>(null);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const f = acceptedFiles[0];
        setFile(f);
        setResult(null);
        setError(null);

        // Create preview URL for images/videos
        if (f.type.startsWith('image/') || f.type.startsWith('video/')) {
            const objectUrl = URL.createObjectURL(f);
            setPreview(objectUrl);
        } else {
            setPreview(null);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': [],
            'video/*': [],
            'audio/*': []
        }
    });

    const handleAnalyze = async () => {
        if (!file) return;

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        try {
            // Assuming backend runs on port 8000 on localhost
            const endpoint = 'http://localhost:8000/analyze/upload';
            const res = await axios.post(endpoint, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setResult(res.data);
        } catch (err) {
            console.error(err);
            setError("Analysis Failed. Ensure the backend server is running on port 8000.");
        } finally {
            setLoading(false);
        }
    };

    const getResultAsset = () => {
        if (!result) return null;
        if (result.verdict === 'REAL') {
            return (
                <div className="flex flex-col items-center animate-in fade-in zoom-in duration-500">
                    <img src="/assets/Videos/man.gif" alt="Real" className="w-64 h-64 object-contain mb-4 rounded-xl shadow-lg border-4 border-green-500/50" />
                    <div className="text-3xl font-bold text-green-500 flex items-center gap-2">
                        <CheckCircle className="w-8 h-8" /> Verified Real
                    </div>
                    <p className="text-muted-foreground mt-2">No manipulation detected.</p>
                </div>
            );
        } else {
            return (
                <div className="flex flex-col items-center animate-in fade-in zoom-in duration-500">
                    <img src="/assets/Videos/ai-assistant.gif" alt="Fake" className="w-64 h-64 object-contain mb-4 rounded-xl shadow-lg border-4 border-red-500/50" />
                    <div className="text-3xl font-bold text-red-500 flex items-center gap-2">
                        <AlertTriangle className="w-8 h-8" /> {result.verdict} DETECTED
                    </div>
                    <p className="text-muted-foreground mt-2">
                        High probability of AI manipulation ({Math.round(result.final_score * 100)}%).
                    </p>
                </div>
            );
        }
    };

    return (
        <Layout>
            <div className="container mx-auto py-12 px-4 max-w-5xl">
                <header className="mb-12 text-center space-y-4">
                    <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
                        Deepfake Inspector
                    </h1>
                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                        Advanced forensic analysis for digital media. Detect AI-generated content with state-of-the-art neural networks.
                    </p>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">

                    {/* Upload Section */}
                    <div className="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 shadow-2xl">
                        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2">
                            <Upload className="w-6 h-6 text-primary" /> Upload Media
                        </h2>

                        <div
                            {...getRootProps()}
                            className={`
                border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300
                flex flex-col items-center justify-center min-h-[300px]
                ${isDragActive ? 'border-primary bg-primary/10 scale-[1.02]' : 'border-muted-foreground/30 hover:border-primary/50 hover:bg-muted/5'}
              `}
                        >
                            <input {...getInputProps()} />
                            {file ? (
                                <div className="space-y-4">
                                    {preview && (
                                        file.type.startsWith('video') ?
                                            <video src={preview} className="max-h-48 mx-auto rounded shadow-md" controls /> :
                                            <img src={preview} alt="Preview" className="max-h-48 mx-auto rounded shadow-md" />
                                    )}
                                    <div className="flex items-center gap-2 justify-center text-lg font-medium">
                                        <File className="w-5 h-5" /> {file.name}
                                    </div>
                                    <p className="text-sm text-muted-foreground">Click to change file</p>
                                </div>
                            ) : (
                                <>
                                    <div className="w-20 h-20 bg-muted/20 rounded-full flex items-center justify-center mb-6">
                                        <Upload className="w-10 h-10 text-muted-foreground" />
                                    </div>
                                    <p className="text-xl font-medium mb-2">Drag & drop or Click to Upload</p>
                                    <p className="text-sm text-muted-foreground">
                                        Supports Video (MP4, AVI), Audio (WAV, MP3), and Images
                                    </p>
                                </>
                            )}
                        </div>

                        {file && (
                            <button
                                onClick={handleAnalyze}
                                disabled={loading}
                                className="w-full mt-6 bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg py-4 rounded-xl shadow-lg transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
                            >
                                {loading ? <Loader2 className="animate-spin w-6 h-6" /> : "Analyze Media"}
                            </button>
                        )}

                        {error && (
                            <div className="mt-6 p-4 bg-destructive/10 text-destructive rounded-lg flex items-center gap-3 border border-destructive/20">
                                <AlertCircle className="w-5 h-5" /> {error}
                            </div>
                        )}
                    </div>

                    {/* Result Section */}
                    <div className="bg-card/50 backdrop-blur-sm border border-border/50 rounded-2xl p-8 shadow-2xl min-h-[500px] flex flex-col relative overflow-hidden">

                        <h2 className="text-2xl font-semibold mb-6 flex items-center gap-2 z-10">
                            <CheckCircle className="w-6 h-6 text-primary" /> Analysis Result
                        </h2>

                        <div className="flex-1 flex flex-col items-center justify-center z-10">
                            {loading ? (
                                <div className="text-center space-y-4">
                                    <div className="w-64 h-64 mx-auto">
                                        <Lottie animationData={faceRecognitionData} loop={true} />
                                    </div>
                                    <p className="text-xl font-medium animate-pulse text-primary">Scanning for artifacts...</p>
                                    <p className="text-sm text-muted-foreground">Analyzing compression traces and inconsistencies</p>
                                </div>
                            ) : result ? (
                                getResultAsset()
                            ) : (
                                <div className="text-center text-muted-foreground/50 space-y-4">
                                    <div className="w-32 h-32 border-4 border-dashed border-muted-foreground/20 rounded-full mx-auto flex items-center justify-center">
                                        <File className="w-12 h-12" />
                                    </div>
                                    <p>Results will appear here after analysis</p>
                                </div>
                            )}
                        </div>

                        {/* Background Decoration */}
                        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl -z-0 translate-x-1/2 -translate-y-1/2 pointer-events-none" />
                        <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/5 rounded-full blur-3xl -z-0 -translate-x-1/2 translate-y-1/2 pointer-events-none" />

                    </div>
                </div>

                {result && (
                    <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 animate-in slide-in-from-bottom duration-700 delay-200">
                        <div className="bg-card/30 border border-border/50 p-6 rounded-xl">
                            <div className="text-sm text-muted-foreground mb-1">Visual Manipulation Score</div>
                            <div className="text-3xl font-mono font-bold">{(result.visual_score * 100).toFixed(1)}%</div>
                            <div className="w-full bg-muted/30 h-2 mt-3 rounded-full overflow-hidden">
                                <div className="h-full bg-blue-500 transition-all duration-1000" style={{ width: `${result.visual_score * 100}%` }} />
                            </div>
                        </div>
                        <div className="bg-card/30 border border-border/50 p-6 rounded-xl">
                            <div className="text-sm text-muted-foreground mb-1">Audio Manipulation Score</div>
                            <div className="text-3xl font-mono font-bold">{(result.audio_score * 100).toFixed(1)}%</div>
                            <div className="w-full bg-muted/30 h-2 mt-3 rounded-full overflow-hidden">
                                <div className="h-full bg-purple-500 transition-all duration-1000" style={{ width: `${result.audio_score * 100}%` }} />
                            </div>
                        </div>
                        <div className="bg-card/30 border border-border/50 p-6 rounded-xl">
                            <div className="text-sm text-muted-foreground mb-1">Overall Confidence</div>
                            <div className={`text-3xl font-mono font-bold ${result.final_score > 0.5 ? 'text-red-400' : 'text-green-400'}`}>
                                {(result.final_score * 100).toFixed(1)}%
                            </div>
                        </div>
                    </div>
                )}

            </div>
        </Layout>
    );
};

export default DeepfakeDetector;
