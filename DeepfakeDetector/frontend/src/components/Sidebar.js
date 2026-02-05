import { Image, Video, Mic, Link, FileText, Activity } from 'lucide-react'

export default function Sidebar({ activeTab, setActiveTab }) {
    const menuItems = [
        { id: 'image', label: 'Image Analysis', icon: <Image size={20} /> },
        { id: 'video', label: 'Video Analysis', icon: <Video size={20} /> },
        { id: 'audio', label: 'Audio Analysis', icon: <Mic size={20} /> },
        { id: 'url', label: 'URL Scanner', icon: <Link size={20} /> },
        { id: 'report', label: 'Reports', icon: <FileText size={20} /> },
    ]

    return (
        <aside className="w-64 bg-cardbg border-r border-gray-800 flex flex-col">
            <div className="p-6 flex items-center space-x-2 border-b border-gray-800">
                <Activity className="text-primary" size={32} />
                <span className="text-xl font-bold tracking-tight">DeepVerify</span>
            </div>

            <nav className="flex-1 p-4 space-y-2">
                {menuItems.map((item) => (
                    <button
                        key={item.id}
                        onClick={() => setActiveTab(item.id)}
                        className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors duration-200 ${activeTab === item.id
                                ? 'bg-primary text-white shadow-lg shadow-primary/20'
                                : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                            }`}
                    >
                        {item.icon}
                        <span className="font-medium">{item.label}</span>
                    </button>
                ))}
            </nav>

            <div className="p-4 border-t border-gray-800">
                <div className="bg-gray-900 rounded-lg p-3 text-xs text-gray-500">
                    <p>System Status: <span className="text-green-500">Online</span></p>
                    <p>Model: Hybrid V2 (CPU)</p>
                </div>
            </div>
        </aside>
    )
}
