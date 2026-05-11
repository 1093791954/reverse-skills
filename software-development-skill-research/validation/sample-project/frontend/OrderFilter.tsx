type Props = {
  status: string;
  onStatusChange: (status: string) => void;
  isLoading: boolean;
};

export function OrderFilter({ status, onStatusChange, isLoading }: Props) {
  return (
    <form>
      <label htmlFor="status">Order status</label>
      <select
        id="status"
        value={status}
        disabled={isLoading}
        onChange={(event) => onStatusChange(event.target.value)}
      >
        <option value="">All</option>
        <option value="open">Open</option>
        <option value="closed">Closed</option>
      </select>
      {isLoading ? <p role="status">Loading orders...</p> : null}
    </form>
  );
}
