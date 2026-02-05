import Head from 'next/head'
import { useState } from 'react'
import { Upload, Link, AlertTriangle } from 'lucide-react'
import Sidebar from '../components/Sidebar'
import AnalysisTab from '../components/AnalysisTab'
import ReportTab from '../components/ReportTab'

export default function Home() {
    const [activeTab, setActiveTab] = useState('image')

    return (
        <div className="flex min-h-screen bg-darkbg text-white font-sans">
            <Head>
                <title>Deepfake Detective Platform</title>
            </Head>

            {/* Sidebar */}
            <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

            {/* Main Content */}
            <main className="flex-1 p-8">
                <div className="max-w-6xl mx-auto">
                    <header className="mb-8">
                        <h1 className="text-3xl font-bold mb-2">Forensic Analysis Dashboard</h1>
                        <p className="text-gray-400">Police-Grade Hybrid Detection System (CPU Optimized)</p>
                    </header>

                    {/* Dynamic Content */}
                    <div className="bg-cardbg rounded-xl border border-gray-800 min-h-[600px] p-6 shadow-2xl">
                        {activeTab === 'image' && <AnalysisTab type="image" title="Image Forensics" icon={<Upload />} />}
                        {activeTab === 'video' && <AnalysisTab type="video" title="Video Forensics" icon={<Upload />} />}
                        {activeTab === 'audio' && <AnalysisTab type="audio" title="Audio Forensics" icon={<Upload />} />}
                        {activeTab === 'url' && <AnalysisTab type="url" title="URL Intelligence" icon={<Link />} />}
                        {activeTab === 'report' && <ReportTab />}
                    </div>
                </div>
            </main>
        </div>
    )
}
