const CreateRoomForm = () => {
    const handleSubmit = () =>{
        alert("submitted")
    }
  return (
    <div className="w-1/2 h-auto flex flex-col p-4 gap-6 bg-[white] rounded-lg shadow-lg">
      <h1 className="font-semibold capitalize">Create Room</h1>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <input
          type="text"
          className="w-full p-2 border border-slate-300 placeholder:text-sm"
          placeholder="room name..."
        />
        <select className="w-full p-2 border border-slate-300 text-sm">
          <option value="Community" className="text-sm flex">
            Community
          </option>
          <option value="Group" className="text-sm flex">
            Group
          </option>
        </select>

        <button className="w-full p-2 flex items-center justify-center bg-black text-white cursor-pointer">
          Create
        </button>
      </form>
    </div>
  );
};

export default CreateRoomForm;
