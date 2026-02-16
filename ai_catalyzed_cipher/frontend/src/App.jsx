import { useEffect, useState } from 'react'
import { Line } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js'
import api from './services/api'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend)

export default function App() {
  const [values, setValues] = useState('1.0,2.0,3.0')
  const [recordId, setRecordId] = useState(null)
  const [noise, setNoise] = useState(null)
  const [benchmark, setBenchmark] = useState(null)

  useEffect(() => {
    api.get('/benchmark').then((r) => setBenchmark(r.data)).catch(() => null)
    api.get('/noise-prediction').then((r) => setNoise(r.data.predicted_noise)).catch(() => null)
  }, [])

  const encrypt = async () => {
    const payload = { label: 'dashboard-record', values: values.split(',').map((v) => Number(v.trim())) }
    const res = await api.post('/encrypt', payload)
    setRecordId(res.data.record_id)
  }

  const chartData = {
    labels: benchmark ? ['Encrypt', 'Add', 'Multiply'] : [],
    datasets: [{
      label: 'Latency (ms)',
      data: benchmark ? [benchmark.encrypt_ms, benchmark.add_ms, benchmark.mul_ms] : [],
      borderColor: '#38bdf8',
      backgroundColor: '#38bdf8'
    }]
  }

  return (
    <div className="min-h-screen p-6 bg-slate-950 text-slate-100">
      <h1 className="text-3xl font-bold mb-6">AI-Catalyzed Cipher Dashboard</h1>
      <div className="grid md:grid-cols-2 gap-6">
        <section className="bg-slate-900 p-4 rounded-xl">
          <h2 className="font-semibold text-xl mb-2">Encryption dashboard</h2>
          <input className="w-full p-2 rounded bg-slate-800" value={values} onChange={(e) => setValues(e.target.value)} />
          <button className="mt-3 px-4 py-2 rounded bg-cyan-600" onClick={encrypt}>Encrypt</button>
          <p className="mt-3">Latest record ID: {recordId ?? 'N/A'}</p>
        </section>

        <section className="bg-slate-900 p-4 rounded-xl">
          <h2 className="font-semibold text-xl mb-2">Noise Budget Visualization</h2>
          <p>Predicted noise: {noise ?? 'loading...'}</p>
          {benchmark && <Line data={chartData} />}
        </section>
      </div>

      <section className="mt-6 bg-slate-900 p-4 rounded-xl">
        <h2 className="font-semibold text-xl mb-2">Query execution interface</h2>
        <p>Use API endpoint <code>/execute-secure-query</code> with IDs from encrypted records.</p>
      </section>
    </div>
  )
}
