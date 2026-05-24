const colors = {
  pending:  { bg: '#fff3cd', text: '#856404' },
  reviewed: { bg: '#cce5ff', text: '#004085' },
  accepted: { bg: '#d4edda', text: '#155724' },
  rejected: { bg: '#f8d7da', text: '#721c24' },
}

export default function StatusBadge({ status }) {
  const color = colors[status] || colors.pending
  return (
    <span style={{
      backgroundColor: color.bg,
      color: color.text,
      padding: '4px 10px',
      borderRadius: '12px',
      fontSize: '13px',
      fontWeight: '600',
      textTransform: 'capitalize'
    }}>
      {status}
    </span>
  )
}
