const { getCpuPercent, setup } = require("./main");
jest.useFakeTimers();

jest.mock("axios");

describe("setup", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("axios post should be called with correct payload", async () => {
    const axios = require("axios");
    axios.post.mockResolvedValue({ data: {} });

    await setup("test-app");

    expect(axios.post).toHaveBeenCalledTimes(1);
    expect(axios.post).toHaveBeenCalledWith("http://api:54321/api/apps", {
      appName: "test-app",
      language: "JavaScript",
      cpuModel: expect.any(String),
      cores: expect.any(Number),
    });
  });
});
