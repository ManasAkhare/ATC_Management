DROP TABLE IF EXISTS public.aircraft CASCADE;
DROP TABLE IF EXISTS public.flight CASCADE;
DROP TABLE IF EXISTS public.schedule CASCADE;
DROP TABLE IF EXISTS public.crew CASCADE;
DROP TABLE IF EXISTS public.flight_data CASCADE;
DROP TABLE IF EXISTS public.plane_commercial CASCADE;
DROP TABLE IF EXISTS public.plane_private CASCADE;
DROP TABLE IF EXISTS public.plane_info CASCADE;
DROP TABLE IF EXISTS public.route_info CASCADE;
DROP TABLE IF EXISTS public.user_flight_mapping CASCADE;

--
-- PostgreSQL database dump
--


-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: aircraft; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.aircraft (
    plane_number character varying(10) NOT NULL,
    plane_type character varying(50),
    manufacturer character varying(50),
    flight_type character(15)
);


ALTER TABLE public.aircraft OWNER TO postgres;

--
-- Name: crew; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.crew (
    flight_number character varying(10),
    crew_size integer,
    pilot character varying(100),
    copilot character varying(100),
    crew_id character varying(5) NOT NULL
);


ALTER TABLE public.crew OWNER TO postgres;

--
-- Name: flight; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flight (
    flight_number character varying(10) NOT NULL,
    airline_company character varying(50),
    departure_airport character varying(50),
    arrival_airport character varying(50),
    passenger_number integer,
    status character(15)
);

ALTER TABLE ONLY public.flight FORCE ROW LEVEL SECURITY;


ALTER TABLE public.flight OWNER TO postgres;

--
-- Name: flight_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.flight_data (
    id integer NOT NULL,
    xml_content xml
);


ALTER TABLE public.flight_data OWNER TO postgres;

--
-- Name: flight_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.flight_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.flight_data_id_seq OWNER TO postgres;

--
-- Name: flight_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.flight_data_id_seq OWNED BY public.flight_data.id;


--
-- Name: plane_commercial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plane_commercial (
    plane_number character varying(10),
    plane_type character varying(20),
    manufacturer character(20),
    flight_type character(15)
);


ALTER TABLE public.plane_commercial OWNER TO postgres;

--
-- Name: plane_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plane_info (
    flight_number character varying(10),
    airline_company character(20),
    passenger_number integer
);


ALTER TABLE public.plane_info OWNER TO postgres;

--
-- Name: plane_private; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.plane_private (
    plane_number character varying(10),
    plane_type character varying(20),
    manufacturer character(20),
    flight_type character(15)
);


ALTER TABLE public.plane_private OWNER TO postgres;

--
-- Name: route_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.route_info (
    flight_number character varying(10),
    departure_airport character(20),
    arrival_airport character(20),
    status character(15)
);


ALTER TABLE public.route_info OWNER TO postgres;

--
-- Name: schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.schedule (
    flight_number character varying(10) NOT NULL,
    departure_time time without time zone,
    arrival_time time without time zone,
    runway_number integer,
    terminal_number character varying(3)
);


ALTER TABLE public.schedule OWNER TO postgres;

--
-- Name: user_flight_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_flight_mapping (
    username character varying(50) NOT NULL,
    flight_number character varying(10) NOT NULL
);


ALTER TABLE public.user_flight_mapping OWNER TO postgres;

--
-- Name: flight_data id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flight_data ALTER COLUMN id SET DEFAULT nextval('public.flight_data_id_seq'::regclass);


--
-- Data for Name: aircraft; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.aircraft
INSERT INTO public.aircraft (plane_number, plane_type, manufacturer, flight_type) VALUES
('VT-IFV', 'Airbus A321neo', 'Airbus', 'Commercial     '),
('VT-ALQ', 'Boeing 787', 'Boeing', 'Commercial     '),
('VT-SGB', 'Boeing 737 Max', 'Boeing', 'Commercial     '),
('VT-TNC', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-HMN', 'Gulfstream G650', 'Gulfstream', 'Private        '),
('VT-VJR', 'Bombardier Global', 'Bombardier', 'Private        '),
('VT-IBA', 'Airbus A320', 'Airbus', 'Commercial     '),
('VT-ANR', 'Boeing 787', 'Boeing', 'Commercial     '),
('VT-AXN', 'Boeing 737', 'Boeing', 'Commercial     '),
('VT-VNS', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-JSW', 'Falcon 2000', 'Dassault', 'Private        '),
('VT-TID', 'Airbus A321', 'Airbus', 'Commercial     '),
('VT-SGE', 'Boeing 737', 'Boeing', 'Commercial     '),
('VT-AIK', 'Boeing 777', 'Boeing', 'Commercial     '),
('VT-INN', 'Airbus A320', 'Airbus', 'Commercial     '),
('VT-GMR', 'Cessna Latitude', 'Textron', 'Private        '),
('VT-VKB', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-IJK', 'Airbus A321neo', 'Airbus', 'Commercial     '),
('VT-ALM', 'Boeing 777', 'Boeing', 'Commercial     '),
('VT-AXP', 'Boeing 737', 'Boeing', 'Commercial     '),
('VT-VLA', 'Airbus A319', 'Airbus', 'Commercial     '),
('VT-RLN', 'Embraer Legacy', 'Embraer', 'Private        '),
('VT-IFO', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-ANK', 'Boeing 787', 'Boeing', 'Commercial     '),
('VT-SGZ', 'Boeing 737 Max', 'Boeing', 'Commercial     '),
('VT-TNJ', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-AMB', 'Falcon 8X', 'Dassault', 'Private        '),
('VT-TNK', 'Airbus A321neo', 'Airbus', 'Commercial     '),
('VT-SGL', 'Boeing 737', 'Boeing', 'Commercial     '),
('VT-AIL', 'Boeing 777', 'Boeing', 'Commercial     '),
('VT-IPI', 'Airbus A320', 'Airbus', 'Commercial     '),
('VT-SRK', 'Gulfstream G550', 'Gulfstream', 'Private        '),
('VT-VKC', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-ILM', 'Airbus A321neo', 'Airbus', 'Commercial     '),
('VT-ALZ', 'Boeing 787', 'Boeing', 'Commercial     '),
('VT-AXR', 'Boeing 737', 'Boeing', 'Commercial     '),
('VT-VLC', 'Airbus A319', 'Airbus', 'Commercial     '),
('VT-PNK', 'Bombardier Challenger', 'Bombardier', 'Private        '),
('VT-IFP', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-ANL', 'Boeing 787', 'Boeing', 'Commercial     '),
('VT-SHA', 'Boeing 737 Max', 'Boeing', 'Commercial     '),
('VT-TNL', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-TNM', 'Airbus A321neo', 'Airbus', 'Commercial     '),
('VT-SGM', 'Boeing 737', 'Boeing', 'Commercial     '),
('VT-AIM', 'Boeing 777', 'Boeing', 'Commercial     '),
('VT-IPJ', 'Airbus A320', 'Airbus', 'Commercial     '),
('VT-BIR', 'Cessna CJ4', 'Textron', 'Private        '),
('VT-VKD', 'Airbus A320neo', 'Airbus', 'Commercial     '),
('VT-ILN', 'Airbus A321neo', 'Airbus', 'Commercial     '),
('VT-AMA', 'Gulfstream G280', 'Gulfstream', 'Private        ');



--
-- Data for Name: crew; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.crew
INSERT INTO public.crew (flight_number, crew_size, pilot, copilot, crew_id) VALUES
('6E2134', '6', 'Capt. Rajesh Khanna', 'FO Amit Shah', 'C501'),
('AI805', '10', 'Capt. Sandeep Verma', 'FO Priya Nair', 'C502'),
('SG123', '5', 'Capt. Vikram Singh', 'FO Anjali Rao', 'C503'),
('UK944', '7', 'Capt. Rohan Mehra', 'FO Sneha Gupta', 'C504'),
('PVT001', '2', 'Capt. Sameer Reddy', 'FO Akash Malhotra', 'C505'),
('PVT002', '2', 'Capt. Neha Sharma', 'FO Rahul Deshmukh', 'C506'),
('6E5321', '6', 'Capt. Ishaan Iyer', 'FO Kavita Reddy', 'C507'),
('AI101', '12', 'Capt. Suresh Raina', 'FO Manish Pandey', 'C508'),
('UK812', '6', 'Capt. Virat Kohli', 'FO KL Rahul', 'C509'),
('SG445', '5', 'Capt. MS Dhoni', 'FO Rohit Sharma', 'C510'),
('6E125', '6', 'Capt. Hardik Pandya', 'FO Jasprit Bumrah', 'C511'),
('QP1102', '6', 'Capt. Shikhar Dhawan', 'FO Rishabh Pant', 'C512'),
('AI420', '8', 'Capt. Ravindra Jadeja', 'FO Axar Patel', 'C513'),
('6E998', '6', 'Capt. Shreyas Iyer', 'FO Ishan Kishan', 'C514'),
('UK707', '7', 'Capt. Shubman Gill', 'FO Suryakumar Yadav', 'C515'),
('PVT003', '2', 'Capt. Ravi Shastri', 'FO Rahul Dravid', 'C516'),
('SG881', '5', 'Capt. Sunil Gavaskar', 'FO Kapil Dev', 'C517'),
('6E442', '6', 'Capt. Anil Kumble', 'FO Harbhajan Singh', 'C518'),
('AI330', '9', 'Capt. Sourav Ganguly', 'FO VVS Laxman', 'C519'),
('UK611', '7', 'Capt. Sachin Tendulkar', 'FO Zaheer Khan', 'C520'),
('QP1205', '6', 'Capt. Gautam Gambhir', 'FO Yuvraj Singh', 'C521'),
('6E303', '6', 'Capt. Virender Sehwag', 'FO Irfan Pathan', 'C522'),
('AI671', '8', 'Capt. Ashish Nehra', 'FO Bhuvneshwar Kumar', 'C523'),
('UK981', '6', 'Capt. Mohammed Shami', 'FO Umesh Yadav', 'C524'),
('PVT004', '2', 'Capt. Kuldeep Yadav', 'FO Yuzvendra Chahal', 'C525'),
('SG221', '5', 'Capt. Prithvi Shaw', 'FO Devdutt Padikkal', 'C526'),
('6E505', '6', 'Capt. Sanju Samson', 'FO Deepak Hooda', 'C527'),
('AI992', '8', 'Capt. Rahul Tewatia', 'FO Shivam Dube', 'C528'),
('UK822', '7', 'Capt. Venkatesh Iyer', 'FO Nitish Rana', 'C529'),
('QP1300', '6', 'Capt. Varun Chakravarthy', 'FO Prasidh Krishna', 'C530'),
('6E712', '6', 'Capt. Arshdeep Singh', 'FO Harshal Patel', 'C531'),
('PVT005', '2', 'Capt. Deepak Chahar', 'FO Shardul Thakur', 'C532'),
('AI123', '9', 'Capt. Ravi Bishnoi', 'FO Avesh Khan', 'C533'),
('UK551', '6', 'Capt. Umran Malik', 'FO T Natarajan', 'C534'),
('SG707', '5', 'Capt. Jaydev Unadkat', 'FO Cheteshwar Pujara', 'C535'),
('6E881', '6', 'Capt. Ajinkya Rahane', 'FO Hanuma Vihari', 'C536'),
('AI554', '8', 'Capt. Mayank Agarwal', 'FO Karun Nair', 'C537'),
('UK442', '6', 'Capt. Wriddhiman Saha', 'FO Ishant Sharma', 'C538'),
('PVT006', '2', 'Capt. Murali Vijay', 'FO Dinesh Karthik', 'C539'),
('QP1402', '6', 'Capt. Ambati Rayudu', 'FO Parthiv Patel', 'C540'),
('6E909', '6', 'Capt. Robin Uthappa', 'FO Amit Mishra', 'C541'),
('AI881', '7', 'Capt. Piyush Chawla', 'FO Vinay Kumar', 'C542'),
('UK221', '6', 'Capt. Pragyan Ojha', 'FO Munaf Patel', 'C543'),
('SG332', '5', 'Capt. RP Singh', 'FO S Sreesanth', 'C544'),
('6E112', '6', 'Capt. Yusuf Pathan', 'FO Naman Ojha', 'C545'),
('AI772', '8', 'Capt. Ashok Dinda', 'FO Manoj Tiwary', 'C546'),
('UK101', '6', 'Capt. Mohit Sharma', 'FO Sandeep Sharma', 'C547'),
('PVT007', '2', 'Capt. Vijay Shankar', 'FO Krunal Pandya', 'C548'),
('QP1505', '6', 'Capt. Washington Sundar', 'FO Rahul Chahar', 'C549'),
('6E404', '6', 'Capt. Shahbaz Ahmed', 'FO Mukesh Kumar', 'C550');



--
-- Data for Name: flight; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.flight
INSERT INTO public.flight (flight_number, airline_company, departure_airport, arrival_airport, passenger_number, status) VALUES
('6E2134', 'IndiGo', 'DEL', 'BOM', '180', 'On-Time        '),
('AI805', 'Air India', 'BOM', 'BLR', '245', 'Boarding       '),
('SG123', 'SpiceJet', 'MAA', 'DEL', '142', 'Delayed        '),
('UK944', 'Vistara', 'DEL', 'HYD', '158', 'Scheduled      '),
('PVT001', 'Reliance Transport', 'BOM', 'DEL', '8', 'On-Time        '),
('PVT002', 'Adani Aviation', 'AMD', 'BOM', '5', 'Scheduled      '),
('6E5321', 'IndiGo', 'PNQ', 'CCU', '178', 'On-Time        '),
('AI101', 'Air India', 'DEL', 'JFK', '310', 'On-Time        '),
('UK812', 'Vistara', 'BLR', 'DEL', '162', 'Scheduled      '),
('SG445', 'SpiceJet', 'CCU', 'MAA', '130', 'Delayed        '),
('6E125', 'IndiGo', 'HYD', 'BOM', '170', 'On-Time        '),
('QP1102', 'Akasa Air', 'BLR', 'AMD', '172', 'Cancelled      '),
('AI420', 'Air India', 'DEL', 'COK', '150', 'On-Time        '),
('6E998', 'IndiGo', 'LKO', 'DEL', '182', 'Scheduled      '),
('UK707', 'Vistara', 'CCU', 'BOM', '144', 'On-Time        '),
('PVT003', 'JSW Steel', 'DEL', 'MAA', '10', 'On-Time        '),
('SG881', 'SpiceJet', 'BOM', 'GOI', '120', 'On-Time        '),
('6E442', 'IndiGo', 'COK', 'BLR', '175', 'Delayed        '),
('AI330', 'Air India', 'MAA', 'BOM', '220', 'On-Time        '),
('UK611', 'Vistara', 'BOM', 'HYD', '155', 'Scheduled      '),
('QP1205', 'Akasa Air', 'MAA', 'BLR', '165', 'On-Time        '),
('6E303', 'IndiGo', 'DEL', 'PNQ', '170', 'On-Time        '),
('AI671', 'Air India', 'BOM', 'MAA', '200', 'Boarding       '),
('UK981', 'Vistara', 'DEL', 'AMD', '140', 'Scheduled      '),
('PVT004', 'GMR Aviation', 'DEL', 'HYD', '6', 'On-Time        '),
('SG221', 'SpiceJet', 'DEL', 'BOM', '135', 'Delayed        '),
('6E505', 'IndiGo', 'BLR', 'HYD', '180', 'On-Time        '),
('AI992', 'Air India', 'HYD', 'DEL', '190', 'Scheduled      '),
('UK822', 'Vistara', 'BOM', 'DEL', '160', 'On-Time        '),
('QP1300', 'Akasa Air', 'AMD', 'DEL', '168', 'On-Time        '),
('6E712', 'IndiGo', 'MAA', 'CCU', '172', 'Scheduled      '),
('PVT005', 'Poonawalla Av.', 'PNQ', 'BOM', '4', 'On-Time        '),
('AI123', 'Air India', 'CCU', 'DEL', '210', 'On-Time        '),
('UK551', 'Vistara', 'HYD', 'BLR', '150', 'Delayed        '),
('SG707', 'SpiceJet', 'BOM', 'PNQ', '115', 'On-Time        '),
('6E881', 'IndiGo', 'AMD', 'MAA', '177', 'Scheduled      '),
('AI554', 'Air India', 'BLR', 'BOM', '230', 'Boarding       '),
('UK442', 'Vistara', 'DEL', 'CCU', '148', 'On-Time        '),
('PVT006', 'Birla Group', 'BOM', 'CCU', '7', 'Scheduled      '),
('QP1402', 'Akasa Air', 'DEL', 'BLR', '174', 'On-Time        '),
('6E909', 'IndiGo', 'CCU', 'HYD', '170', 'On-Time        '),
('AI881', 'Air India', 'PNQ', 'DEL', '185', 'Delayed        '),
('UK221', 'Vistara', 'MAA', 'BOM', '152', 'Scheduled      '),
('SG332', 'SpiceJet', 'HYD', 'DEL', '138', 'On-Time        '),
('6E112', 'IndiGo', 'BOM', 'DEL', '185', 'On-Time        '),
('AI772', 'Air India', 'DEL', 'MAA', '215', 'Scheduled      '),
('UK101', 'Vistara', 'BLR', 'MAA', '155', 'On-Time        '),
('PVT007', 'Ambani Aviation', 'AMD', 'DEL', '9', 'On-Time        '),
('QP1505', 'Akasa Air', 'BOM', 'HYD', '160', 'Scheduled      '),
('6E404', 'IndiGo', 'DEL', 'COK', '178', 'On-Time        ');



--
-- Data for Name: flight_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.flight_data
INSERT INTO public.flight_data (id, xml_content) VALUES
('1', '<FlightCatalog>\n    <Flight>\n        <FlightNumber>6E2134</FlightNumber>\n        <Airline>IndiGo</Airline>\n        <Departure>DEL</Departure>\n        <Arrival>BOM</Arrival>\n        <Status>On-Time</Status>\n    </Flight>\n    <Flight>\n        <FlightNumber>AI805</FlightNumber>\n        <Airline>Air India</Airline>\n        <Departure>BOM</Departure>\n        <Arrival>BLR</Arrival>\n        <Status>Boarding</Status>\n    </Flight>\n    <Flight>\n        <FlightNumber>6E5321</FlightNumber>\n        <Airline>IndiGo</Airline>\n        <Departure>PNQ</Departure>\n        <Arrival>CCU</Arrival>\n        <Status>On-Time</Status>\n    </Flight>\n    <Flight>\n        <FlightNumber>SG123</FlightNumber>\n        <Airline>SpiceJet</Airline>\n        <Departure>MAA</Departure>\n        <Arrival>DEL</Arrival>\n        <Status>Delayed</Status>\n    </Flight>\n    <Flight>\n        <FlightNumber>UK944</FlightNumber>\n        <Airline>Vistara</Airline>\n        <Departure>BOM</Departure>\n        <Arrival>HYD</Arrival>\n        <Status>Scheduled</Status>\n    </Flight>\n</FlightCatalog>');



--
-- Data for Name: plane_commercial; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.plane_commercial
INSERT INTO public.plane_commercial (plane_number, plane_type, manufacturer, flight_type) VALUES
('VT-IFV', 'Airbus A321neo', 'Airbus              ', 'Commercial     '),
('VT-ALQ', 'Boeing 787', 'Boeing              ', 'Commercial     '),
('VT-SGB', 'Boeing 737 Max', 'Boeing              ', 'Commercial     '),
('VT-TNC', 'Airbus A320neo', 'Airbus              ', 'Commercial     ');



--
-- Data for Name: plane_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.plane_info
INSERT INTO public.plane_info (flight_number, airline_company, passenger_number) VALUES
('6E2134', 'IndiGo              ', '180'),
('AI805', 'Air India           ', '245'),
('SG123', 'SpiceJet            ', '142'),
('UK944', 'Vistara             ', '158'),
('PVT001', 'Reliance Transport  ', '8'),
('PVT002', 'Adani Aviation      ', '5');



--
-- Data for Name: plane_private; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.plane_private
INSERT INTO public.plane_private (plane_number, plane_type, manufacturer, flight_type) VALUES
('VT-HMN', 'Gulfstream G650', 'Gulfstream          ', 'Private        '),
('VT-VJR', 'Bombardier Global', 'Bombardier          ', 'Private        ');



--
-- Data for Name: route_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.route_info
INSERT INTO public.route_info (flight_number, departure_airport, arrival_airport, status) VALUES
('6E2134', 'DEL                 ', 'BOM                 ', 'On-Time        '),
('AI805', 'BOM                 ', 'BLR                 ', 'Boarding       '),
('SG123', 'MAA                 ', 'DEL                 ', 'Delayed        '),
('UK944', 'DEL                 ', 'HYD                 ', 'Scheduled      '),
('PVT001', 'BOM                 ', 'DEL                 ', 'On-Time        '),
('PVT002', 'AMD                 ', 'BOM                 ', 'Scheduled      ');



--
-- Data for Name: schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.schedule
INSERT INTO public.schedule (flight_number, departure_time, arrival_time, runway_number, terminal_number) VALUES
('6E2134', '07:15:00', '09:30:00', '28', 'T3'),
('AI805', '18:45:00', '20:30:00', '9', 'T2'),
('SG123', '13:00:00', '15:45:00', '10', 'T1'),
('UK944', '10:20:00', '12:35:00', '27', 'T3'),
('PVT001', '09:00:00', '11:15:00', '14', 'GA'),
('PVT002', '16:30:00', '17:45:00', '27', 'GA'),
('6E5321', '21:50:00', '00:15:00', '14', 'T2'),
('AI101', '02:00:00', '15:30:00', '28', 'T3'),
('UK812', '06:45:00', '09:15:00', '11', 'T2'),
('SG445', '14:20:00', '16:50:00', '9', 'T1'),
('6E125', '11:00:00', '12:30:00', '10', 'T1'),
('QP1102', '08:00:00', '10:15:00', '11', 'T1'),
('AI420', '15:30:00', '18:45:00', '27', 'T3'),
('6E998', '19:00:00', '20:15:00', '10', 'T2'),
('UK707', '17:15:00', '20:00:00', '14', 'T2'),
('PVT003', '08:30:00', '11:45:00', '28', 'GA'),
('SG881', '07:00:00', '08:15:00', '9', 'T1'),
('6E442', '12:45:00', '14:00:00', '11', 'T2'),
('AI330', '10:00:00', '12:15:00', '14', 'T2'),
('UK611', '14:50:00', '16:30:00', '27', 'T2'),
('QP1205', '09:20:00', '10:45:00', '10', 'T1'),
('6E303', '16:15:00', '18:30:00', '28', 'T3'),
('AI671', '13:00:00', '15:00:00', '9', 'T2'),
('UK981', '11:30:00', '13:15:00', '11', 'T3'),
('PVT004', '15:00:00', '17:30:00', '14', 'GA'),
('SG221', '18:10:00', '20:25:00', '27', 'T1'),
('6E505', '19:45:00', '21:00:00', '10', 'T1'),
('AI992', '06:00:00', '08:15:00', '28', 'T1'),
('UK822', '20:30:00', '22:45:00', '9', 'T2'),
('QP1300', '07:30:00', '09:15:00', '11', 'T2'),
('6E712', '14:00:00', '16:45:00', '14', 'T1'),
('PVT005', '11:15:00', '12:00:00', '27', 'GA'),
('AI123', '05:30:00', '08:00:00', '10', 'T2'),
('UK551', '17:45:00', '19:00:00', '28', 'T1'),
('SG707', '08:15:00', '09:30:00', '9', 'T1'),
('6E881', '21:00:00', '23:50:00', '11', 'T2'),
('AI554', '12:00:00', '13:45:00', '14', 'T2'),
('UK442', '15:15:00', '18:00:00', '27', 'T3'),
('PVT006', '10:45:00', '13:30:00', '10', 'GA'),
('QP1402', '19:30:00', '22:15:00', '28', 'T3'),
('6E909', '06:45:00', '08:30:00', '9', 'T2'),
('AI881', '13:15:00', '15:30:00', '11', 'T2'),
('UK221', '09:45:00', '11:50:00', '14', 'T1'),
('SG332', '16:00:00', '18:15:00', '27', 'T1'),
('6E112', '18:50:00', '21:05:00', '10', 'T2'),
('AI772', '20:15:00', '23:15:00', '28', 'T3'),
('UK101', '07:30:00', '08:45:00', '9', 'T1'),
('PVT007', '12:20:00', '14:15:00', '11', 'GA'),
('QP1505', '14:40:00', '16:10:00', '14', 'T2'),
('6E404', '22:30:00', '01:45:00', '27', 'T3');



--
-- Data for Name: user_flight_mapping; Type: TABLE DATA; Schema: public; Owner: postgres
--

-- Insert data for public.user_flight_mapping
INSERT INTO public.user_flight_mapping (username, flight_number) VALUES
('aditya', '6E2134'),
('parth', 'SG123'),
('rajesh', 'PVT001');



--
-- Name: flight_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.flight_data_id_seq', 1, true);


--
-- Name: aircraft aircraft_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.aircraft
    ADD CONSTRAINT aircraft_pkey PRIMARY KEY (plane_number);


--
-- Name: crew crew_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.crew
    ADD CONSTRAINT crew_pkey PRIMARY KEY (crew_id);


--
-- Name: flight_data flight_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flight_data
    ADD CONSTRAINT flight_data_pkey PRIMARY KEY (id);


--
-- Name: flight flight_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.flight
    ADD CONSTRAINT flight_pkey PRIMARY KEY (flight_number);


--
-- Name: schedule schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.schedule
    ADD CONSTRAINT schedule_pkey PRIMARY KEY (flight_number);


--
-- Name: user_flight_mapping user_flight_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_flight_mapping
    ADD CONSTRAINT user_flight_mapping_pkey PRIMARY KEY (username, flight_number);


--
-- Name: idx_departure_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_departure_time ON public.schedule USING btree (departure_time);


--
-- Name: idx_flight_num; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_flight_num ON public.flight USING btree (flight_number);


--
-- Name: idx_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_status ON public.flight USING btree (status);


--
-- Name: flight; Type: ROW SECURITY; Schema: public; Owner: postgres
--

ALTER TABLE public.flight ENABLE ROW LEVEL SECURITY;

--
-- Name: flight passenger_mapping_policy; Type: POLICY; Schema: public; Owner: postgres
--

CREATE POLICY passenger_mapping_policy ON public.flight FOR SELECT TO passenger USING (((flight_number)::text IN ( SELECT user_flight_mapping.flight_number
   FROM public.user_flight_mapping
  WHERE ((user_flight_mapping.username)::text = CURRENT_USER))));


--
-- Name: TABLE aircraft; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.aircraft TO admin;
GRANT SELECT ON TABLE public.aircraft TO atc;


--
-- Name: TABLE crew; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.crew TO admin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.crew TO atc;
GRANT SELECT ON TABLE public.crew TO passenger;


--
-- Name: TABLE flight; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.flight TO admin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.flight TO atc;
GRANT SELECT ON TABLE public.flight TO passenger;


--
-- Name: TABLE plane_commercial; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.plane_commercial TO admin;


--
-- Name: TABLE plane_info; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.plane_info TO admin;


--
-- Name: TABLE plane_private; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.plane_private TO admin;


--
-- Name: TABLE route_info; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.route_info TO admin;


--
-- Name: TABLE schedule; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.schedule TO admin;
GRANT SELECT,INSERT,UPDATE ON TABLE public.schedule TO atc;
GRANT SELECT ON TABLE public.schedule TO passenger;


--
-- Name: TABLE user_flight_mapping; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT ON TABLE public.user_flight_mapping TO passenger;


--
-- PostgreSQL database dump complete
--


