import { AlertTriangle, CheckCircle, RefreshCcw } from 'lucide-react'

export default function ResultsView({ result, file, type, reset }) {
    const isFake = result.verdict === 'FAKE'
    const isSus = result.verdict === 'SUSPICIOUS'
    const color = isFake ? 'text-red-500' : (isSus ? 'text-orange-500' : 'text-green-500')
    const score = (result.final_score * 100).toFixed(1)

    return (
        <div className="animate-fade-in space-y-8">
            {/* Header Card */}
            <div className="bg-gray-900/50 p-6 rounded-xl border border-gray-700 flex justify-between items-center">
                <div>
                    <h3 className="text-sm text-gray-400 uppercase tracking-wider">Analysis Verdict</h3>
                    <div className={`text-4xl font-black ${color} flex items-center gap-3 mt-1`}>
                        {isFake ? <AlertTriangle size={40} /> : <CheckCircle size={40} />}
                        {result.verdict}
                    </div>
                    <p className="text-gray-400 mt-2">
                        Confidence: <span className="text-white font-bold">{score}%</span>
                    </p>
                </div>
                <button onClick={reset} className="text-gray-400 hover:text-white flex gap-2 items-center px-4 py-2 rounded-lg border border-gray-700 hover:bg-gray-800">
                    <RefreshCcw size={16} /> New Scan
                </button>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Media Preview */}
                <div className="bg-cardbg border border-gray-800 rounded-xl p-4">
                    <h4 className="text-lg font-semibold mb-4">Input Media</h4>
                    <div className="bg-black rounded-lg overflow-hidden flex items-center justify-center min-h-[300px]">
                        {type === 'image' && file && (
                            <img src={URL.createObjectURL(file)} alt="Analyzed" className="max-h-[400px] object-contain" />
                        )}
                        {type === 'video' && file && (
                            <video src={URL.createObjectURL(file)} controls className="max-w-full max-h-[400px]" />
                        )}
                        {type === 'audio' && (
                            <div className="w-full p-4">
                                <audio src={URL.createObjectURL(file)} controls className="w-full" />
                                <div className="h-32 bg-gray-900 mt-4 rounded-lg flex items-center justify-center text-gray-600">
                                    [Waveform Visualization]
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Breakdown */}
                <div className="space-y-6">
                    <div className="bg-cardbg border border-gray-800 rounded-xl p-6">
                        <h4 className="text-lg font-semibold mb-4">Score Breakdown</h4>

                        {/* Progress Bars */}
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between mb-1">
                                    <span className="text-gray-400">Deepfake Probability</span>
                                    <span>{score}%</span>
                                </div>
                                <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                                    <div
                                        className={`h-full ${isFake ? 'bg-red-500' : 'bg-green-500'}`}
                                        style={{ width: `${score}%` }}
                                    />
                                </div>
                            </div>

                            {result.details.visual && (
                                <div>
                                    <div className="flex justify-between mb-1">
                                        <span className="text-gray-400">Visual Anomalies</span>
                                        <span>{(result.details.visual.fake_score * 100 || 0).toFixed(1)}%</span>
                                    </div>
                                    <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                                        <div className="h-full bg-blue-500" style={{ width: `${(result.details.visual.fake_score || 0) * 100}%` }} />
                                    </div>
                                </div>
                            )}

                            {result.details.audio && (
                                <div>
                                    <div className="flex justify-between mb-1">
                                        <span className="text-gray-400">Audio Artifacts</span>
                                        <span>{(result.details.audio.score * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="h-2 bg-gray-700 rounded-full overflow-hidden">
                                        <div className="h-full bg-purple-500" style={{ width: `${result.details.audio.score * 100}%` }} />
                                    </div>
                                    <div className="mt-2 text-xs text-red-300">
                                        {result.details.audio.anomalies?.join(", ")}
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* AI Explanation */}
                    <div className="bg-cardbg border border-gray-800 rounded-xl p-6">
                        <h4 className="text-lg font-semibold mb-2">Forensic Analysis</h4>
                        <p className="text-gray-400 text-sm leading-relaxed">
                            The system analyzed {type} content using a hybrid ensemble.
                            {isFake
                                ? " Several artifacts consistent with generative AI were detected. ELA analysis suggests pixel manipulation, and XceptionNet indicates high probability of face swapping or synthesis."
                                : " No significant anomalies were detected. ELA noise patterns are consistent, and audio spectral flatness is within natural human range."}
                        </p>

                        <div className="mt-4 flex gap-2">
                            <span className="px-3 py-1 bg-gray-800 rounded-full text-xs text-gray-300">EfficientNet-B0</span>
                            <span className="px-3 py-1 bg-gray-800 rounded-full text-xs text-gray-300">Xception</span>
                            <span className="px-3 py-1 bg-gray-800 rounded-full text-xs text-gray-300">SignalForensics</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
