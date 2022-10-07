import global_variable from "@/utils/global_variable.js"

test("global_variable", () => {
    expect(global_variable.url).toBe("http://49.232.101.156:8000")
})