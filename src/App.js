import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { Login } from "./components/Auth/login";
import Register from "../src/components/Auth/Register";
import {
  AuthProvider,
  AuthConsumer,
} from "./components/context/JWTAuthContext";
import { Flex, Spinner } from "@chakra-ui/react";
import { NavBar } from "./components/Navbar/navbar";
import { PublicRoute } from "./components/Auth/PublicRoute";
import { Authenticated } from "./components/Auth/Authenticated";
import { TodoList } from "./components/Todo/ToDoList";
import { TodoDetail } from "./components/Todo/TodoDetail";

function App() {
  return (
    <>
      <AuthProvider>
        <Router>
          <AuthConsumer>
            {(auth) =>
              !auth.isInitialized ? (
                <Flex
                  height="100vh"
                  alignItems="center"
                  justifyContent="center"
                >
                  <Spinner
                    thickness="5px"
                    speed="0.5"
                    emptyColor="green.300"
                    color="green.500"
                    size="lg"
                  />
                </Flex>
              ) : (
                <Routes>
                  <Route
                    path="/login"
                    element={
                      <PublicRoute>
                        <Login />
                      </PublicRoute>
                    }
                  />
                  <Route
                    path="/register"
                    element={
                      <PublicRoute>
                        <Register />
                      </PublicRoute>
                    }
                  />
                  <Route path="/" element={<NavBar />}>
                    <Route
                      path="/"
                      element={
                        <Authenticated>
                          <TodoList />
                        </Authenticated>
                      }
                    ></Route>
                    <Route
                      path="/:todoId"
                      element={
                        <Authenticated>
                          <TodoDetail />
                        </Authenticated>
                      }
                    />
                  </Route>
                  <Route path="*" element={<Navigate to="/" />} />
                </Routes>
              )
            }
          </AuthConsumer>
        </Router>
      </AuthProvider>
    </>
  );
}

export default App;
